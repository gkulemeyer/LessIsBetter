import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster
 
############### SUBSAMPLING METHODS ###############

############ randS ############

def randS(data, max_sequences, random_state=42): 
    ids = []
    for fam in data.fam.unique():
        meta_fam = data.query('fam == @fam').copy() 
        if meta_fam.shape[0] > max_sequences:
            ids.append(meta_fam.sample(max_sequences, random_state=random_state).index) # RANDOM SAMPLE (PD)
        else:
            ids.append(meta_fam.index)
    return pd.Series(np.concatenate(ids))


############ clusS ############

def clusS(data, distances, max_sequences=0): 

    distances_intra_fam = intra_distances(data, distances)

    ids = []
    for fam, matrix_intra in distances_intra_fam.items():
        fam_ids = clusS_by_fam(matrix_intra, max_sequences)
        ids.append(fam_ids) 
    return pd.Series(np.concatenate(ids))

def clusS_by_fam(matrix_intra, max_sequences=0):
    if max_sequences <= 0:
        raise ValueError("max_sequences must be > 0")
   
    D = matrix_intra.copy()
    if D.shape[0] <= max_sequences:
        return D.index 

    ids = D.index

    Z = linkage(squareform(D.values, checks=False), method="average")
    labels = fcluster(Z, t=max_sequences, criterion="maxclust")  

    # Medoide por clúster
    reps = []
    for cluster_id in np.unique(labels):
        members = np.where(labels == cluster_id)[0]
        medoid = medoid_of_cluster(D.values, members)
        reps.append(ids[medoid])
    
    return reps

def medoid_of_cluster(distances, members):
    """
    D          : matriz de distancias (ndarray n×n)
    members    : índices (int) dentro de D que pertenecen al clúster
    Devuelve   : índice (int) del miembro que minimiza la ∑ distancia.
    """
    if len(members) == 1:
        return members[0]
    sub = distances[np.ix_(members, members)]
    medoid_idx = np.argmin(sub.sum(axis=1))
    return members[medoid_idx] 

############ sortS ############

def sortS(data, distances, max_sequences=0): 

    distances_intra_fam = intra_distances(data, distances)

    ids = []
    for fam, matrix_intra in distances_intra_fam.items():
        fam_ids = sortS_by_fam(matrix_intra, max_sequences)
        ids.append(fam_ids) 
    return pd.Series(np.concatenate(ids))
 
def sortS_by_fam(matrix_intra, max_sequences=0):

    assert max_sequences >= 0, "max_sequences must be positive"
    M = matrix_intra.copy()
    np.fill_diagonal(M.values, np.nan) 
    if M.shape[0] < max_sequences: 
        return M.index

    min_val = np.nanmin(M.values)
    while M.shape[0] > max_sequences:
        min_val = np.nanmin(M.values)
        count = (M == min_val).sum(axis=1).values
        drop_idx = np.argmax(count)
        drop_label = M.index[drop_idx]   
        M = M.drop(index=drop_label, columns=drop_label)  
    return M.index

############ ##### ############
############ UTILS ############

def intra_distances(data: pd.DataFrame, distances: pd.DataFrame):
    """
    Devuelve dict {fam: sub-matrix de distancias}.
    """
    common = sorted(set(distances.index) & set(data.index))
    distances = distances.loc[common, common]
    data = data.loc[common]
    if len(distances.index) != len(data.index):
        print(f"Warning: distance matrix has {len(distances.index)} entries but data has {len(data.index)}.")
        print(f"Aligning by 'id'... {len(common)} common entries found.")
        
    idx_fam = data.groupby("fam").groups
    return {fam: distances.loc[ids, ids].copy() for fam, ids in idx_fam.items()}

def load_distances(path): 
    try:
        distances = pd.read_hdf(path)  
        return distances
    except Exception as e:
        raise RuntimeError(
            f"Could not load distance matrix from {path}. "
            "Make sure the file exists and PyTables is installed."
        ) from e