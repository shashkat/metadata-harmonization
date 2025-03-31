# Main features:
# - We will do sentence-meaning matching at two levels, columns and values in a particular column
# - Any time we are doing sentence-meaning matching, we will try to 
#       - check for negations, so that we don't mistakenly match opposites.
#       - make UMAP showing where the values lie, which will help the end user making decision if it was right or not.
# - At the end, we will use pandas-profiling (ydata-profiling), to generate a comparison report between the curated and modification of the new dataset.

# imports
from sentence_transformers import SentenceTransformer, util
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# read in the two metadatas as dataframe
curated_md = pd.read_csv('data/curated_meta.csv', low_memory=False)
new_md = pd.read_csv('data/new_meta.csv')


#################### STEP 0: GET THE COLUMN TYPES ###############

# first, get the numerical cols
numerical_cols = []
for col in curated_md.columns:
    if curated_md[col].dtype == float or curated_md['age_max'].dtype == int:
        numerical_cols.append(col)

# For other cols, lets first make a histogram of teh number of unique values in each column. 
# This may help us in determining a threshold for unique values, to decide a column to be 
# categorical or not.

# dict in which we will store the number of unique values for each col
num_unique_vals_all = {}
for col in curated_md.columns:
    # ignore the numerical cols
    if col in numerical_cols: continue

    # the number of unique values in this col
    num_unique_vals = len(curated_md[col].unique())
    num_unique_vals_all[col] = num_unique_vals

# make the barplot of num_unique_values in each col
sns.barplot(num_unique_vals_all, orient='h')
plt.show()

# the few columns which could be non-categorical after looking at the plot are:
# biomarker, feces_phenotype_value, disease, disease_ontology_term, treatment, treatment_ontology_term, unmetadata
# but it turns out that only biomarker seems to fit the non categorical category most well.




