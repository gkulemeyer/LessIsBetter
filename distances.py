import subprocess
import numpy as np
import pandas as pd
from tqdm import tqdm
from parser import build_distance_parser
 

def compute_distances(data):
    ids = data.index
    distances = pd.DataFrame(np.zeros((len(ids), len(ids))))-1
    distances.index, distances.columns = ids, ids 

    for i,rowi in tqdm(data.iterrows(),total=len(data)):
        for j,rowj in data.iterrows():
            if distances.loc[j,i] < 0:
                echo_line = rowi.structure + "\n" + rowj.structure
                # RNAdistance cannot handle pseudoknots (treated as unpaired) https://pubmed.ncbi.nlm.nih.gov/36077037/
                echo_line = echo_line.replace('<','.').replace('>','.').replace('{','.').replace('}','.')
                oo = subprocess.check_output(["RNAdistance"], input=echo_line.encode('utf-8'))

                if oo != b"":
                    max_len = len(rowi.structure) if len(rowi.structure)>len(rowj.structure) else len(rowj.structure) 
                    distances.loc[i,j] = float(oo[2:])/max_len
                else:
                    distances.loc[i,j] = np.nan
                    print("Warning: RNAdistance error with {} and {}".format(i, j))
            else:
                distances.loc[i,j] = distances.loc[j,i]
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