from __future__ import annotations

import argparse
import json
import random
import re
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

BASE = "https://db.chgk.info"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
HEADERS = {"User-Agent": UA}
DIFF_MAP = {
    1: "Очень простой",
    2: "Простой",
    3: "Средний",
    4: "Сложный",
    5: "Очень сложный",
}


def build_url(difficulty: int, limit: int = 24, types: str = "1") -> str:
    seed = random.randint(10**8, 2_147_483_647)
    return f"{BASE}/random/answers/types{types}/complexity{difficulty}/{seed}/limit{limit}"

def fetch_html(url: str, max_retries: int = 4, backoff: float = 1.5) -> str:
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200 and "Вопрос" in r.text:
                return r.text
        except Exception as e:
            last_exc = e
        time.sleep(backoff * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}") from last_exc

_Q_ANCHOR_RE = re.compile(r"Вопрос\s*\d+\s*:", flags=re.I)

def split_into_blocks(page_text: str) -> List[str]:
    idxs = [m.start() for m in _Q_ANCHOR_RE.finditer(page_text)]
    blocks = []
    for i, start in enumerate(idxs):
        end = idxs[i+1] if i + 1 < len(idxs) else len(page_text)
        blocks.append(page_text[start:end].strip())
    return blocks

def _extract_first(pattern: str, text: str, flags=0, default: Optional[str] = None) -> Optional[str]:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default

def parse_block(block: str) -> Dict:
    b = re.sub(r"[ \t]+\n", "\n", block)

    first_line = b.split("\n", 1)[0].strip()
    date = _extract_first(r"\b(\d{4}-\d{2}-\d{2})\b", first_line)

    question = None
    m_q = re.search(r"Вопрос\s*\d+\s*:\s*(.+?)(?=\nОтвет:|\n\.\.\.\n|\Z)", b, flags=re.S)
    if m_q:
        question = m_q.group(1).strip()

    def until_next(label: str) -> Optional[str]:
        pat = rf"{label}:\s*(.+?)(?=\n(?:Зач[её]т|Комментарий|Источник|Автор:|Вопрос\s*\d+\s*:)|\Z)"
        return _extract_first(pat, b, flags=re.S)

    answer   = until_next("Ответ")
    notes   = until_next("Зач[её]т")
    comment  = until_next("Комментарий")
    sourcesb = until_next("Источник\(и\)") 
    authors  = _extract_first(r"\nАвтор:\s*(.+)", b)

    sources: List[str] = []
    if sourcesb:
        for line in sourcesb.strip().splitlines():
            clean = re.sub(r"^\s*[\d\.\-\•\)]\s*", "", line).strip()
            if clean:
                sources.append(clean)

    result_raw = _extract_first(r"\nРезультат:\s*([^\n]+)", b)
    result_score = None
    result_total = None
    if result_raw:
        m = re.search(r"(\d+)\s*/\s*(\d+)", result_raw)
        if not m:
            m = re.search(r"(\d+)\s*из\s*(\d+)", result_raw, flags=re.I)
        if m:
            result_score, result_total = int(m.group(1)), int(m.group(2))

    return {
        "tour": first_line,
        "date": date,
        "question": question,
        "answer": answer,
        "notes": notes,
        "comment": comment,
        "sources": sources,
        "authors": authors,
        "result": result_raw,
        "result_score": result_score,
        "result_total": result_total,
    }

def parse_page(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    blocks = split_into_blocks(text)
    out: List[Dict] = []
    for b in blocks:
        rec = parse_block(b)
        if rec.get("question") and rec.get("answer"):
            out.append(rec)
    return out

def norm_key(q: str, a: str) -> str:
    def norm(s: str) -> str:
        s = s or ""
        s = s.lower()
        s = re.sub(r"\s+", " ", s)
        s = s.strip()
        return s
    return norm(q) + " || " + norm(a)

def scrape_difficulty(difficulty: int,
                      target: int = 1000,
                      batch_limit: int = 24,
                      max_requests: int = 200,
                      sleep: float = 1.0) -> Dict:

    seen = set()
    data: List[Dict] = []
    attempts = 0

    while len(data) < target and attempts < max_requests:
        url = build_url(difficulty=difficulty, limit=batch_limit)
        html = fetch_html(url)
        items = parse_page(html)

        added = 0
        for it in items:
            q, a = it.get("question"), it.get("answer")
            if not q or not a:
                continue
            key = norm_key(q, a)
            if key in seen:
                continue
            seen.add(key)
            data.append({
                "id": f"chgk_{uuid.uuid4().hex[:10]}",
                **it,
                "difficulty": DIFF_MAP.get(difficulty, str(difficulty)),
                "difficulty_id": difficulty,
                "source_url": url,
            })
            added += 1

        attempts += 1
        time.sleep(sleep)

        print(f"[d={difficulty}] batch {attempts}: +{added} (total {len(data)}/{target})")

        if added == 0:
            time.sleep(sleep * 2)

    return {
        "metadata": {
            "source": "random/answers/types1/complexity{d}/seed/limit{batch}",
            "difficulty": DIFF_MAP.get(difficulty, str(difficulty)),
            "difficulty_id": difficulty,
            "size": len(data),
        },
        "data": data,
    }

def save_json(obj: Dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True, help="Output directory")
    ap.add_argument("--target", type=int, default=1000, help="Target # per difficulty")
    ap.add_argument("--batch-limit", type=int, default=24, help="Per-request batch size")
    ap.add_argument("--difficulties", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    ap.add_argument("--max-requests", type=int, default=250, help="Safety cap on requests per difficulty")
    ap.add_argument("--sleep", type=float, default=1.0, help="Seconds between requests")
    args = ap.parse_args()

    for d in args.difficulties:
        print(f"[scrape] difficulty={d} ({DIFF_MAP.get(d)}) → target={args.target} (batch {args.batch_limit})")
        obj = scrape_difficulty(
            difficulty=d,
            target=args.target,
            batch_limit=args.batch_limit,
            max_requests=args.max_requests,
            sleep=args.sleep,
        )
        save_json(obj, args.outdir / f"chgk_random_d{d}.json")
        print(f"[save] d={d} size={obj['metadata']['size']} → {args.outdir / f'chgk_random_d{d}.json'}")

    print("done")

if __name__ == "__main__":
    main()
