import subprocess
import numpy as np
import pandas as pd
from tqdm import tqdm
import RNA
from parser import build_distance_parser
 


def structure_to_tree(struc):
    # RNAdistance cannot handle pseudoknots (treated as unpaired)
    #  https://pubmed.ncbi.nlm.nih.gov/36077037/
    struc = struc.translate(str.maketrans("<>{}", "...."))

    tree_string = RNA.db_to_tree_string(
        struc,
        RNA.STRUCTURE_TREE_EXPANDED,
    )
    return RNA.make_tree(tree_string)

def compute_distances(data):
    ids = data.index

    trees = {
        idx: structure_to_tree(row.structure)
        for idx, row in data.iterrows()
    }

    lengths = data["structure"].str.len().to_dict()

    distances = pd.DataFrame( np.zeros((len(ids), len(ids))),index=ids,columns=ids) -1

    for k, i in enumerate(tqdm(ids)):
        distances.loc[i, i] = 0.
        for j in ids[k + 1:]:
            distance = RNA.tree_edit_distance(trees[i], trees[j])

            if distance < 0:
                value = np.nan
                print(f"Warning: RNAdistance error with {i} and {j}")
            else:
                value = distance / max(lengths[i], lengths[j])

            distances.loc[i, j] = value
            distances.loc[j, i] = value

    return distances

def main():

    args = build_distance_parser() 

    data = pd.read_csv(args.file_path, index_col="id")
    if "structure" not in data.columns:
        raise SystemExit("[ERROR]: data must have 'structure' column") 
    
    dist = compute_distances(data)
    args.save_path.mkdir(parents=True, exist_ok=True)
    dist.to_hdf(args.save_path / f"{args.file_path.stem}_distances.h5", key='rnadist', mode='w')


if __name__ == "__main__":
    main()