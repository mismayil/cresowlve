EXTERNAL_MATERIAL_ANNOTATION = (
    "You are a strict annotator. Your task is to decide whether the given puzzle EXPLICITLY instructs the participant to check external materials to answer the question.\n\n"
    "Answer \"yes\" ONLY if the puzzle requires explicit external resource lookup, such as:\n"
    " - A handout (\"раздаточный материал\") or statements like \"на розданной вам фотографии\", \"смотрите раздатку\", \"не озвучивать текст раздатки\", \"в раздатке\", or similar.\n"
    " - References to a hidden or closed element such as: \"мы закрыли символ\", \"мы закрыли букву\", \"мы закрыли часть текста\", \"прочерк\", when the missing content is NOT provided within the puzzle text.\n"
    " - Instructions requiring external lookup such as \"зайдите по ссылке и посмотрите курс\", \"вставьте число из источника\", etc.\n\n"
    "Answer \"no\" if:\n"
    " - The puzzle does not EXPLICITLY instruct the participant to check external materials.\n"
    "Output ONLY 'yes' or 'no' in lowercase, with no additional text.\n\n"
    "Puzzle:\n{question}\n\n"
    "Additional notes:\n{comment}\n\n"
    "Answer:"
)

TRANSLATE_PUZZLE_RU_TO_EN = (
    "You are a professional Russian to English translator. Your task is to translate "
    "Russian puzzles into English with absolute fidelity.\n\n"
    "Translate EXACTLY, preserving:\n"
    "- all logical clues\n"
    "- all named entities\n"
    "- sentence order and structure\n"
    "- rhetorical devices\n"
    "- ambiguity\n"
    "- references and style\n"
    "- the puzzle's original difficulty\n\n"
    "Do NOT:\n"
    "- paraphrase\n"
    "- simplify or summarize\n"
    "- interpret hidden meanings\n"
    "- add explanations\n"
    "- rephrase stylistically\n\n"
    "If a segment is unclear, translate it literally.\n\n"
    "You are given the puzzle question, answer, comment and notes in Russian enclosed in <Question>, <Answer>, <Comment>, and <Notes> tags.\n"
    "Translate each section into English, preserving the structure and meaning, and output the translated puzzle in the same format with <Question>, <Answer>, <Comment>, and <Notes> tags.\n\n"
    "Output ONLY the English translation, nothing else.\n\n"
    "Russian Puzzle:\n<Question>{question}</Question>\n<Answer>{answer}</Answer>\n<Comment>{comment}</Comment>\n<Notes>{notes}</Notes>\n"
    "English Translation:"
)

RUSSIAN_SPECIFIC_ANNOTATION_INSTR = (
    "You are a strict annotator. You are given a puzzle in Russian, along with its answer, comment, and notes and translation of the puzzle into English."
    "Your task is to decide whether the puzzle can not be solved in English because solving the puzzle REQUIRES knowledge specific to the Russian LANGUAGE.\n\n"
    "Answer 'yes' ONLY if the solution depends on Russian-specific linguistic features such as:\n"
    "- idioms, sayings, or set expressions that break in translation\n"
    "- wordplay, puns, or jokes that work ONLY in Russian\n"
    "- Russian-specific homonyms or near-homonyms\n"
    "- phonetic or rhyming clues that exist ONLY in Russian\n"
    "- letter-based tricks involving the Russian alphabet or spelling\n"
    "- translating the puzzle into another language would change or destroy the meaning, making the puzzle unsolvable or fundamentally different.\n\n"
    "Answer 'no' if:\n"
    "- the puzzle depends on general knowledge, culture, history, geography, literature, or context, even if these are Russian.\n"
    "- the puzzle uses Russian names/entities but no Russian linguistic tricks\n"
    "- the translated puzzle still is solvable without losing the key idea.\n\n"
    "Given the puzzle question, answer, comment, notes in Russian and the English translation of the puzzle, output your reasoning in English within <Reasoning>...</Reasoning> tags and your answer within <Answer>...</Answer> tags.\n\n"
)

RUSSIAN_SPECIFIC_ANNOTATION_SHOT = (
    "Russian puzzle:\n"
    "Question: {question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Notes: {notes}\n\n"
    "English translation:\n"
    "Question: {question_en}\n"
    "Answer: {answer_en}\n"
    "Comment: {comment_en}\n"
    "Notes: {notes_en}\n\n"
    "<Reasoning>{reasoning}</Reasoning>\n"
    "<Answer>{shot_answer}</Answer>"
)

# English zero-shot CoT for answering in Russian
COT_ONLY_FINAL_ANSWER_RU_EN = (
    "You are an expert in solving creative thinking puzzles. "
    "The puzzle is in Russian. Think step by step and provide ONLY the final answer in Russian, "
    "wrapped in <Answer></Answer> tags.\n"
    "Question:\n{question}"
)

# English zero-shot CoT for answering in English
COT_ONLY_FINAL_ANSWER_EN = (
    "You are an expert in solving creative thinking puzzles. "
    "The puzzle is in English. Think step by step and provide ONLY the final answer in English, "
    "wrapped in <Answer></Answer> tags.\n"
    "Question:\n{question}"
)

# Russian zero-shot template for CoT+answer
COT_ANSWER_RU_EN = (
    "You are an expert at solving creative thinking puzzles. "
    "You are given a puzzle question in Russian that requires creative reasoning over real-world knowledge. "
    "Note that the question might contain several placeholder words (often in all capital case such as ИКС, ИГРЕК, ЭТО, ПЕРВЫЙ, ВТОРОЙ, АЛЬФА, БЕТА, ОН, ОНА, ЕГО, ЕЕ, ОНИ etc.) that substitute for specific entities, objects, or concepts. "
    "These placeholders are crucial for solving the puzzle, and their meaning can only be inferred through careful reasoning about the question. "
    "Given a puzzle question, think step by step and write your reasoning in Russian within <Reasoning>...</Reasoning> tags. "
    "Then provide only the final answer in Russian (unless specified otherwise) within <Answer>...</Answer> tags.\n"
    "Puzzle:\n{question}"
)

# English zero-shot template for CoT+answer
COT_ANSWER_EN = (
    "You are an expert at solving creative thinking puzzles. "
    "You are given a puzzle question that requires creative reasoning over real-world knowledge. "
    "Note that the question might contain several placeholder words (often in all capital case such as X, Y, THIS, FIRST, SECOND, ALPHA, BETA, HE, SHE, IT, HIM, HIS, HER, THEY, THEM etc.) that substitute for specific entities, objects, or concepts. "
    "These placeholders are crucial for solving the puzzle, and their meaning can only be inferred through careful reasoning about the question. "
    "Additionally, some placeholders might be gendered (e.g., HE/HIM/HIS vs SHE/HER), but do not assume that the gendered pronouns necessarily refer to human characters; they could refer to any entities, and their gender might be different. "
    "Given a puzzle question, think step by step and write your reasoning within <Reasoning>...</Reasoning> tags. "
    "Then provide only the final answer within <Answer>...</Answer> tags.\n"
    "Puzzle:\n{question}"
)

# English zero-shot template for reasoning models
REASONING_MODEL_EN = (
    "You are an expert at solving creative thinking puzzles. "
    "You are given a puzzle question that requires creative reasoning over real-world knowledge. "
    "Note that the question might contain several placeholder words (often in all capital case such as X, Y, THIS, FIRST, SECOND, ALPHA, BETA, HE, SHE, IT, HIM, HIS, HER, THEY, THEM etc.) that substitute for specific entities, objects, or concepts. "
    "These placeholders are crucial for solving the puzzle, and their meaning can only be inferred through careful reasoning about the question. "
    "Additionally, some placeholders might be gendered (e.g., HE/HIM/HIS vs SHE/HER), but do not assume that the gendered pronouns necessarily refer to human characters; they could refer to any entities, and their gender might be different. "
    "Please provide your final answer within <Answer>...</Answer> tags.\n"
    "Puzzle:\n{question}"
)

# English zero-shot template for reasoning models
REASONING_MODEL_RU_EN = (
    "You are an expert at solving creative thinking puzzles. "
    "You are given a puzzle question in Russian that requires creative reasoning over real-world knowledge. "
    "Note that the question might contain several placeholder words (often in all capital case such as ИКС, ИГРЕК, ЭТО, ПЕРВЫЙ, ВТОРОЙ, АЛЬФА, БЕТА, ОН, ОНА, ЕГО, ЕЕ, ОНИ etc.) that substitute for specific entities, objects, or concepts. "
    "These placeholders are crucial for solving the puzzle, and their meaning can only be inferred through careful reasoning about the question. "
    "Please provide your final answer in Russian (unless specified otherwise) within <Answer>...</Answer> tags.\n"
    "Puzzle:\n{question}"
)

# llm-as-a-judge with adding context
LLM_JUDGE_WITH_CONTEXT_EN = (
    "You are an expert in judging model responses. Given a question, a reference answer, "
    "a model answer, and additional context such as comments and other acceptable answers, "
    "decide whether the model's answer is correct based on the reference answer and context. "
    "Ignore minor typos, articles, capitalization, and formatting. If the factual core is the same, answer yes. "
    "Also ignore the number of words constraint in the question if the model answer is semantically correct but does not meet the word count requirement. "
    "Answer only: Yes or No.\n\n"
    "Question:\n{question}\n"
    "Reference Answer:\n{answer}\n"
    "Additional Context:\nComments: {comment}\nAcceptable Answers: {notes}\n"
    "Model Answer:\n{prediction}"
)

REASONING_TYPE_ANNOTATION = (
    "You are an expert in annotating type of reasoning involved in solving creative thinking puzzles. "
    "Given a creative thinking puzzle question, its answer, comments about the puzzle and other acceptable answers (if any), do TWO tasks:\n"
    "1) Decide whether solving the puzzle mainly requires SIMPLE FACTUAL reasoning "
    "or CREATIVE ASSOCIATION of distant pieces of knowledge/facts.\n"
    "   - Answer 'factual' when the puzzle is answered by simply retrieving specific facts, "
    "dates, names, or straightforward commonsense reasoning, with no need to make a non-obvious, creative leaps between facts.\n"
    "   - Answer 'creative' when the solver in addition to retrieving the facts, must also make a non-obvious, creative connection, see a hidden twist, "
    "reinterpret words, or combine clues in an indirect way.\n\n"
    "2) If your answer to the previous task is 'CREATIVE', then choose ALL relevant creativity concepts involved in solving the puzzle from the following "
    "list (use EXACT spelling, lowercase):\n"
    "poem, metaphor, idiom, proverb, joke, pun, simile, sarcasm, hyperbole, neologism, "
    "analogy, abstraction, lateral thinking, divergent thinking, commonsense reasoning, compositionality.\n"
    "   - Choose ALL that apply (multi-label).\n"
    "   - If none of the specific labels fit, suggest a list of new labels that are relevant for the puzzle.\n"
    "Carefully read the given puzzle and output:\n"
    "  - One line with the reasoning type: <Answer>factual</Answer> OR <Answer>creative</Answer>.\n"
    "  - If you chose 'creative', on separate lines output ONE OR MORE <concept> tags, "
    "each containing either exactly one label from the allowed list or a new label if you none fits.\n"
    "  - If you chose 'factual', do NOT output any <concept> tags.\n"
)

REASONING_TYPE_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Annotation:\n{shot_answer}"
)

KNOWLEDGE_ANNOTATION = (
    "You are an expert in annotating creative thinking puzzles. "
    "Given a creative thinking puzzle, identify a list of knowledge/facts that are explicitly required to answer the puzzle, and write them in the form of independent questions. "
    "Don't solve the problem. Don't include the answer itself. Wrap each question on a separate line in <knowledge>…</knowledge> tags.\n"
)

KNOWLEDGE_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Knowledge:\n{knowledge}"
)

DOMAIN_ANNOTATION = (
    "You are an expert in annotating creative thinking puzzles. "
    "Given a creative thinking puzzle, its answer, comments about the puzzle and other acceptable answers (if any), identify a list of domains that are involved in solving the puzzle. "
    "A domain is a specific area of knowledge, expertise, or human activity such as physics, literature, sports, music, etc. "
    "Wrap each domain on a separate line in <domain>…</domain> tags.\n"
)

DOMAIN_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Domains:\n{domains}"
)

KNOWLEDGE_SOURCE_ANNOTATION = (
    "You are an expert in annotating creative thinking puzzles. "
    "Given a creative thinking puzzle, its answer, comments about the puzzle and other acceptable answers (if any), determine whether solving the puzzle requires any knowledge related to Russian culture, language, history, geography, or other Russian-specific context. "
    "Note that some questions might mention Russian names, places, or cultural references, but the puzzle can still be solved without any specific knowledge about Russia, so mark them as \"other\". "
    "Answer \"russian\" if the puzzle requires ONLY Russian-specific knowledge, answer \"other\" if the puzzle requires knowledge that is not specific to Russia (or Russians), and answer \"both\" if the puzzle requires both Russian-specific and non-Russian-specific knowledge."
)

KNOWLEDGE_SOURCE_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Knowledge Source: {source}"
)

CULTURE_LANG_ANNOTATION = (
    "You are an expert in annotating creative thinking puzzles. "
    "Given a creative thinking puzzle, its answer, comments about the puzzle and other acceptable answers (if any), identify the languages/cultures that are involved in solving the puzzle. "
    "Output only your final answer and separate them with commas."
)

CULTURE_LANG_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Cultures/Languages: {cultures}"
)

ERROR_ANNOTATION = (
    "You are an expert in categorizing errors in model answers to creative thinking puzzles. "
    "Given a creative thinking puzzle, its answer, comments about the puzzle and other acceptable answers (if any), and model answer and its internal thoughts and final reasoning process, identify the error in model response by assigning it to one of the categories below:\n"
    "1. **Missing creative connection**: A model error where the model fails to recognize the intended associative or metaphorical link between clues, preventing it from making the key conceptual leap needed to reach the correct answer.\n"
    "2. **Overthinking**:The model identifies the correct concept during reasoning, but replaces it with another answer in the final step due to reinterpretation or over-generalization.\n"
    "3. **Hallucination**: The model invents facts, explanations, or source details that are not supported by the question or reliable knowledge and uses them as part of its reasoning. This may include: fabricated facts or entities, invented contextual stories or explanations, or made-up details attributed to real sources or works.\n"
    "4. **Incorrect concept anchoring**: The model locks onto an incorrect concept early and builds reasoning around it, either through associative drift or by reinterpreting the clues to fit that concept.\n"
    "5. **Wrong hypothesis**: The model infers an incorrect rule or shared property from the clues and applies it consistently to produce an answer.\n"
    "6. **Wrong reference**: The model retrieves and reasons about an incorrect work, person, event, or source that superficially matches the clues but is not the intended reference.\n"
    "7. **Clue misinterpretation**: The model identifies the general source, context, or line of reasoning, but selects the wrong specific element required by the clue.\n"
    "Think step by step and provide a brief reasoning inside <Reasoning>...</Reasoning> tags followed by the error category within <Category>...</Category> tags. "
    "If the error does not fit any of the categories, explain the error in the reasoning and suggest a new category name in the answer."
)

ERROR_ANNOTATION_SHOT = (
    "Example {index}:\n"
    "Puzzle:\n{question}\n"
    "Answer: {answer}\n"
    "Comment: {comment}\n"
    "Acceptable Answers: {notes}\n"
    "Model Internal Thoughts:\n{thoughts}\n"
    "Model Reasoning:\n{reasoning}\n"
    "Model Answer:\n{prediction}\n"
    "Error Annotation:\n{annotation}"
)

DATA_CONTAMINATION_GUIDED_EN = (
    "You are provided with a prefix of a question in Russian from the Russian intellectual game \"What? Where? When?\" as found on the website db.chgk.info. "
    "Continue the question exactly as it appears on the website, without any modifications, paraphrasing, or corrections. "
    "Output only the continuation, nothing else.\n"
    "Question: {q_prefix}"
)

DATA_CONTAMINATION_GENERAL_EN = (
    "You are provided with a prefix of a question in Russian. "
    "Continue the question. "
    "Output only the continuation, nothing else.\n"
    "Question: {q_prefix}"
)

DATA_CONTAMINATION_QUIZ_ANNOTATION = (
    "Your task is to create a three-choice quiz by replacing the words in the provided \"Question\" with their contextually relevant synonyms. "
    "The meaning and sentence structure of the three options must exactly match every detail in the Question. You must not include the provided Question as an option. "
    "You must make sure that:\n"
    "(1) You generate distinct options based on the provided Question;\n"
    "(2) The only difference between options is word-level perturbations;\n"
    "(3) There is not any extra explanation;\n"
    "(4) You comply with every specific symbol and letter detail in the given Question; and\n"
    "Given a Question, output three alternative question options and enclose each option with <option>...</option> tags.\n"
    "Question:\n{question}\n"
    "Options:\n"
)

DATA_CONTAMINATION_QUIZ_MCQ = (
    "You are provided with a five-choice quiz. Your task is to correctly select the option that exactly corresponds to an instance "
    "from the What?Where?When (Что? Где? Когда?, also abbreviated as ЧГК or ChGK) game dataset.\n"
    "(1) You must ensure that you only generate a single option letter as your answer.\n"
    "(2) If you do not know the dataset or the correct answer, you must select option E) None of the provided options.\n"
    "Hint: While all the following options seem similar in terms of meaning, there is only one option that reflects the exact wording with respect to the original instance.\n"
    "A) Question: {option_a}\n"
    "B) Question: {option_b}\n"
    "C) Question: {option_c}\n"
    "D) Question: {option_d}\n"
    "E) None of the provided options.\n"
    "Answer:"
)

DATA_CONTAMINATION_QUIZ_BDQ = (
    "You are provided with a five-choice quiz. Your task is to correctly select the option that exactly corresponds to an instance "
    "from the What?Where?When (Что? Где? Когда?, also abbreviated as ЧГК or ChGK) game dataset.\n"
    "(1) You must ensure that you only generate a single option letter as your answer.\n"
    "(2) If you do not know the dataset or the correct answer, you must select option D) None of the provided options.\n"
    "Hint: While all the following options seem similar in terms of meaning, there is only one option that reflects the exact wording with respect to the original instance.\n"
    "A) Question: {option_a}\n"
    "B) Question: {option_b}\n"
    "C) Question: {option_c}\n"
    "D) None of the provided options.\n"
    "Answer:"
)

DATA_CONTAMINATION_QUIZ_BCQ = DATA_CONTAMINATION_QUIZ_BDQ