# The less the better: Improving cross-family RNA secondary structure generalization with structural-aware subsampling

This repository contains a tool to subsample RNA famlilies of a given dataset.  

## Subsampling Strategies

Three strategies are currently implemented in `methods.py`:

- `randS`: random subsampling within each family up to a maximum number of sequences.
- `clusS`: hierarchical clustering within each family using a structural distance matrix, followed by medoid selection of representatives.
- `sortS`: iterative removal based on the smallest pairwise distances within each family .

## Requirements

The repository dependencies are written on `requirements.txt` and can be installed with

```bash
pip install -r requirements.txt
```

## Execution

**main.py**: loads the input file as CSV, if the subsampling method selected is `sortS` or `clusS`, the script also expects the distance matrix as a HDF5 file. Then, it applies one subsampling strategy, and writes the subsampled dataset. Required CSV columns:

- `id`: unique sequence identifier.
- `fam`: RNA family label.

In case the matrix computation is needed, is possible to use the script `distances.py`.

*Arguments*:
- `--file-path`: path to the input CSV file. Default: `data/ArchiveII.csv`
- `--dist-path`: path to the input distance matrix in HDF5 (`.h5`) format. Required for `sortS` and `clusS`. Default: `None`
- `--save-path`: output directory. Default: `outputs`
- `--strategy`: subsampling strategy. Must be one of `randS`, `clusS`, or `sortS`. Default: `randS`
- `--max-sequences`: maximum number of sequences per family. Default: `100`

**distances.py**: given an input CSV file, computes an all-vs-all structural distance matrix using `RNAdistance` and saves in HDF5 format.

- `id`: unique sequence identifier.
- `structure`: secondary structure string (dot bracket format).


*Arguments*:
- `--file-path`: path to the input CSV file. Default: `data/ArchiveII.csv`
- `--save-path`: path to the output directory. If not explicitly provided, the parent directory of `--file-path` is used by default.

**Note:**  `distances.py` calls the [`RNAdistance`](https://github.com/ViennaRNA/ViennaRNA) executable through `subprocess`. This tool must be available in your shell environment before computing structural distances. 


## Usage examples 

### Random subsampling (randS)
 
A minimal command using default configurations is:

```bash
python3 main.py --max-sequences 400
```

While, for a given dataset, `path/to/example.csv`, saving the result in `save/path/`, a command is:

```bash
python3 main.py \ 
  --file-path path/to/example.csv \
  --save-path outputs \
  --strategy save/path/ \
  --max-sequences 400
```

### Structural subsampling (sortS / clusS)

A minimal command using default configurations is:

```bash
python3 main.py \
  --dist-path data/ArchiveII_distances.h5 \
  -- strategy clusS
  --max-sequences 400
```
While, for a given dataset, `path/to/example.csv` with matrix `path/to/distances.h5`, saving the result in `save/path/`, a command is:

```bash
python3 main.py \
  --file-path path/to/example.csv \
  --dist-path path/to/distances.h5 \
  --save-path save/path/ \
  --strategy  randS \
  --max-sequences 100
```
  
### Outputs

`main.py` creates the output directory if needed and saves the subsampled dataset as:

```text
<save-path>/<input_file>_<strategy>_<max_sequences>.csv
```

For example:

```text
outputs/ArchiveII_randS_100.csv
outputs/ArchiveII_clusS_100.csv
outputs/ArchiveII_sortS_100.csv
```

### Compute structural distances

Structural distance computation requires 

```bash
python3 distances.py --file-path data/ArchiveII.csv --save-path data
```
writes the output next to the input CSV and saves:

```text
data/ArchiveII_distances.h5
```

and more generally saves:

```text
data/<input_file>_distances.h5
```

 
