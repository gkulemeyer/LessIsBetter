from pathlib import Path
import argparse

repo_path = Path("/home/gkulemeyer/Documents/DiskB/Guillermo/ImproveInterfam/subsampling/app")
dist_path = repo_path / "data" / "ArchiveII_distances.h5"
file_path = repo_path / "data" / "ArchiveII.csv"
save_path = repo_path / "outputs"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parser for project paths"
    )

    parser.add_argument(
        "--repo-path",
        type=Path,
        default=repo_path,
        help="Path to the repository root"
    )

    parser.add_argument(
        "--file-path",
        type=Path,
        default=None,
        help="Path to the input CSV file. If not provided, data_path / 'ArchiveII.csv' is used"
    )

    parser.add_argument(
        "--dist-path",
        type=Path,
        default=None,
        help="Path to the .h5 distance file. If needed, can be computed with distance.py"
    )

    parser.add_argument(
        "--save-path",
        type=Path,
        default=None,
        help="Output path. If not provided, repo_path / 'app/outputs' is used"
    )

    parser.add_argument(
        "--strategy",
        type=str,
        default="randS",
        choices=["randS", "clusS", "sortS"],
        help="subsampling strategy"
    )

    parser.add_argument(
        "--max-sequences",
        type=int,
        default=100,
        help="Maximum number of sequences per family"
    )

    return parser


def parse_args():
    parser = build_parser()
    args = parser.parse_args() 

    if args.file_path is None:
        print("[WARNING]: No --file-path provided, using default: data/ArchiveII.csv")
        args.file_path = args.repo_path / "data" / "ArchiveII.csv"

    if args.save_path is None:
        args.save_path = args.repo_path / "outputs"

    if args.max_sequences < 0:
        parser.error("--max-sequences must be >= 0")
        
    return args


#### distances ####

def build_distance_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parser for project paths"
    )

    parser.add_argument(
        "--file-path",
        type=Path,
        default=None,
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "--save-path",
        type=Path,
        default=None,
        help="Path to the input CSV file"
    )

    args = parser.parse_args()

    if args.file_path is None:
        parser.error("[ERROR]: No --file-path provided")

    if args.save_path is None:
        print(f"[WARNING]: No --save-path provided, saving on: {args.file_path.parent}")
        args.save_path = args.file_path.parent
    
    return args