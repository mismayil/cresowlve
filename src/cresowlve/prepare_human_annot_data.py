import argparse
import pathlib

from cresowlve.utils import read_json, write_json

def extend_by_source_data(data, source_data_lst):
    for source_data in source_data_lst or []:
        source_data_dict = {item["id"]: item for item in source_data["data"]}
        for sample in data["data"]:
            if sample["id"] in source_data_dict:
                sample.update(source_data_dict[sample["id"]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datapath", type=str, help="Path to task data in json", required=True)
    parser.add_argument("--source-datapaths", nargs="*", type=str, help="Paths to source task data in json")
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="",
        help="Custom suffix for output file path.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="Output directory path. Defaults to input directory path.",
    )
    parser.add_argument("--annot-fields", nargs="*", default=[], help="Fields to include in the answer output")
    parser.add_argument("--num-splits", type=int, default=1, help="Number of splits to divide the data into for separate evaluation files")

    args = parser.parse_args()
    input_data = read_json(args.datapath)
    source_data_lst = [read_json(p) for p in args.source_datapaths] if args.source_datapaths else None

    extend_by_source_data(input_data, source_data_lst)

    datapath = pathlib.Path(args.datapath)
    output_dir = pathlib.Path(args.output_dir) if args.output_dir is not None else datapath.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # split data into specified number of splits for separate evaluation files
    split_size = (len(input_data["data"]) // args.num_splits) + 1
    for i in range(args.num_splits):
        split_data = input_data["data"][i*split_size:(i+1)*split_size]
        output_data = {
                "metadata": {
                    "source": args.datapath,
                    "template": "human_annot",
                    "size": len(split_data),
                    "source_datapaths": args.source_datapaths
                },
                "data": [
                    {
                        **sample,
                        **{field: "" for field in args.annot_fields}
                    }
                    for sample in split_data
                ]
            }

        eval_data_path = output_dir / f"{datapath.stem}_human_annot_split{i}{args.suffix}.json"
        write_json(output_data, eval_data_path)
        print(f"Output data saved to {eval_data_path}")


if __name__ == "__main__":
    main()