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

For example, to perfom structure-aware subsampling using `clusS` on the ArchiveII dataset (default) with an upper limit of 100 elements per family, run:

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


# Reproducibility

The notebooks/ folder contains the code required to reproduce the figures presented in the article.

- **Data distribution**: [Figure 1A](notebooks/Fig1A.ipynb) shows the family distribution in the dataset and the balance. 

- **Distance distributions**: the notebook [Figure 1B](notebooks/Fig1B.ipynb) contains the changes in the intra-family minimum structural distance produced by each subsampling strategy. [Figures 1C and 1D](notebooks/Fig1C-D.ipynb) present the mean and minimum inter- and intra-family distances, and also the impact of the different strategies on the train-to-test distance matrices relative to the full dataset. The intra-family distance matrices at a sequence level and the impact of subsampling are presented in the [Figure 2](notebooks/Fig2.ipynb).

- **Impact on training**: For the different models trained, the [Figure 3](notebooks/Fig3.ipynb) presents the training and validation losses per epoch, and also the F1 score obtained with the validation set and with the family held-out for the different models, and datasets used to train the sincFold model.

- **Impact on generalization**: The test  F1 scores obtained from each model/ strategy/ threshold per family, and a heatmap comparing the performance of each strategy across models and the full dataset is presented in [Figure 4](notebooks/Fig4.ipynb) . Also, [this interactive notebook](https://colab.research.google.com/github/gkulemeyer/LessIsBetter/blob/main/notebooks/Fig4_interactive.ipynb) allows a better comparison between the baseline models and each strategy employed.
