# The less the better: Improving cross-family RNA secondary structure generalization with structural-aware subsampling


This repository contains the source code and data for reproducibility of “The less the better: Improving cross-family RNA secondary structure generalization with structural-aware subsampling,” by G. Kulemeyer, L.A. Bugnon, L. Di Persia, G. Stegmayer, D.H. Milone. Research Institute for Signals, Systems and Computational Intelligence,  [sinc(i)](https://sinc.unl.edu.ar).


In order to improve the generalization capability of deep learning models for RNA secondary structure prediction, three subsampling strategies are proposed. A short summary of each strategy is presented in the table below.


| Strategy | Description    | 
|-------------|--------------| 
| `randS` | random subsampling within each family up to a maximum number of sequences. |
| `clusS` | hierarchical clustering within each family using a structural distance matrix, followed by medoid selection of representatives. |
| `sortS` | iterative removal based on the smallest pairwise distances within each family . | 


## Installation

These steps will guide you through the process of subsampling a secondary structure dataset given.

First:
```
git clone https://github.com/gkulemeyer/LessIsBetter
cd LessIsBetter
```
With a conda working installation, run:

```
conda env create -f environment.yml
```
This should install all required dependencies. Then, activate the environment with:

```
conda activate less-is-better
```

**Note:**  If desired subsampling requires the structural distance, (`sortS` or `clusS`) the script also expects the distance matrix as a HDF5 file.

We provide a script, `distances.py`, to compute the structural distance matrix. This script calls the [`RNAdistance`](https://github.com/ViennaRNA/ViennaRNA) executable through subprocess, so RNAdistance must be available in your shell environment before computing structural distances. The structural distance matrix for the ArchiveII dataset can be downloaded from [this link](https://drive.google.com/file/d/12larI6Glr1uxocJD8RoW3KXXrr0sMYKN/view?usp=drive_link).


## Dataset subsampling 
The `main.py` script loads a dataset from a CSV file with the columns `id` and `fam`, where `fam` indicates the RNA family. The script returns the desired subsampled dataset. 

If the subsampling method selected is `sortS` or `clusS`, the script also requires the structural distance matrix as a HDF5 file. 

For example, to perfom structure-aware subsampling using `clusS` on the ArchiveII dataset (default) with a upper limit of 100 elements per family, run:

```bash
python3 main.py \ 
 --strategy  clusS \
 --dist-path data/ArchiveII_distances.h5 \ 
 --max-sequences 100
```
The output is saved as `outputs/ArchiveII_clusS_100.csv` and is formatted as the input file. For the random subsampling, the `--dist-path` option is not required. 

The `--file-path` option allows to apply the desired subsampling strategy on a custom dataset. The output location can be specified with the `--save-path` option.

The saving pattern is:
```text
<save-path>/<input_file>_<strategy>_<max_sequences>.csv
```

### Compute structural distances


To compute the all-vs-all structural distance matrix, the input dataset must contain the fields `id` and `structure`, where `structure` is given in dot bracket format. 

To compute the matrix, run:

```bash
python3 distances.py \
        --file-path data/ArchiveII.csv \
        --save-path data
```

and returns the output `data/ArchiveII_distances.h5`. If the `--save-path` is not explicitly provided, the parent directory of --file-path is used by default.

**WARNING!** Computing the all-vs-all structural distance matrix may take a long time.

<!-- ____________________________________________________________________ -->


<!-- ## Dataset subsampling 
The `main.py` script loads the dataset as a CSV file with columns `id` and `fam`, and returns the desired subsampled dataset.

For example, to perfom a random subsampling (`randS`) on the ArchiveII dataset (default) with a upper limit of 100 elements per family, run:

```bash
python3 main.py --max-sequences 100
```
The output is formatted as the input file is saved on `outputs/ArchiveII_randS_100.csv`.

To perform a structural subsampling, for example `clusS`, for a given dataset and distance matrix a command is:


```bash
python3 main.py \
 --file-path data/ArchiveII.csv \
 --dist-path outputs/ArchiveII_distances.h5 \
 --save-path outputs/ \
 --strategy  clusS \
 --max-sequences 100
```

The output is formatted as the input file is saved on `outputs/ArchiveII_clusS_100.csv`. -->
<!-- 


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
 --strategy randS \
 --max-sequences 400
```


### Structural subsampling (sortS / clusS)


A minimal command using default configurations is:


```bash
python3 main.py \
 --dist-path data/ArchiveII_distances.h5 \
 --strategy clusS
 --max-sequences 400
```
While, for a given dataset, `path/to/example.csv` with matrix `path/to/distances.h5`, saving the result in `save/path/`, a command is:


```bash
python3 main.py \
 --file-path path/to/example.csv \
 --dist-path path/to/distances.h5 \
 --save-path save/path/ \
 --strategy  clusS \
 --max-sequences 100
```
 ### Outputs


`main.py` creates the output directory if needed and saves the subsampled dataset as:
<save-path>/<input_file>_<strategy>_<max_sequences>.csv


```text
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
writes the output`data/ArchiveII_distances.h5` -->