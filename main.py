import pandas as pd
from parser import parse_args

from methods import clusS, randS, sortS, load_distances   

def main():
    args = parse_args()

    data = pd.read_csv(args.file_path, index_col="id")
    
    if "fam" not in data.columns:
        raise SystemExit("[ERROR]: data must have 'fam' column")

    random_strategy = {"randS": randS}
    distance_strategies = {"clusS": clusS, "sortS": sortS}

    if args.strategy in random_strategy:

        print(f"Applying {args.strategy} subsampling...")
        subsampled_ids = random_strategy[args.strategy](data, args.max_sequences)

    elif args.strategy in distance_strategies:
        
        if args.dist_path is None:
            raise SystemExit(
                "[ERROR]: --dist-path is required for distance-based strategies "
                f"({args.strategy}). The distance.py script computes it."
            )
        distances = load_distances(args.dist_path)

        print(f"Applying {args.strategy} subsampling...")
        subsampled_ids = distance_strategies[args.strategy](
            data, distances, args.max_sequences
        )

    else:
        raise ValueError(f"Unknown strategy: {args.strategy}")

    df_subsampled = data.loc[subsampled_ids]

    print(df_subsampled.groupby("fam").size())

    args.save_path.mkdir(parents=True, exist_ok=True)
    output_file = args.save_path / f"{args.file_path.stem}_{args.strategy}_{args.max_sequences}.csv"
    df_subsampled.to_csv(output_file)

    print(f"Saved subsampled data to: {output_file}")


if __name__ == "__main__":
    main()