# imports
from sentence_transformers import SentenceTransformer, util
import umap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# function to take in two sentences and just print the cos distance between their sentence-transformer embeddings
def GetDistanceBetweenSentences(sentence, query, embedder):
    array1 = embedder.encode(sentence)
    array2 = embedder.encode(query)

    return util.cos_sim(array1, array2).numpy()

# function to make the UMAP to visualize the columns' embeddings of two dataframes, with the option to visualize mappings through lines
def ColumnsUMAP(curated_md, new_md, embedder, fig_width, fig_height, text_size, mapping = None):
    embedding1 = embedder.encode(curated_md.columns)
    embedding2 = embedder.encode(new_md.columns)

    reducer = umap.UMAP()
    embeddings_2d = reducer.fit_transform(np.vstack([embedding1, embedding2]))

    df = pd.DataFrame(data = {
        'x' : embeddings_2d[:,0],
        'y' : embeddings_2d[:,1],
        'cat' : ['curated']*embedding1.shape[0] + ['new']*embedding2.shape[0],
        'col': list(curated_md.columns) + list(new_md.columns)
    })

    # make the base figure
    plt.figure(figsize = (fig_width, fig_height))
    # make the umap
    sns.scatterplot(df, x = 'x', y = 'y', hue = 'cat')
    # add the annotations for the points
    for i in range(len(df)):
        plt.text(x = embeddings_2d[i, 0], y = embeddings_2d[i, 1], s = df['col'][i], ha = 'right', fontsize = text_size)
    
    # if we also want to show lines between mapped columns
    if mapping != None:
        # loop through each entry in the mapping, and draw the corresponding line
        for key in mapping:
            value = mapping[key]
            x1, y1 = embeddings_2d[list(curated_md.columns).index(key), :]
            x2, y2 = embeddings_2d[len(curated_md.columns) + list(new_md.columns).index(value), :]
            plt.plot([x1, x2], [y1, y2], color = 'black', linestyle = 'dashed')
    
    plt.show()
    # clear the figure, so that the legends start from nothing next time we make the figure
    plt.clf() 

# same function as above, just meant for values within a col instead of col names.
def EntriesOFColUMAP(col1_unique_vals, col2_unique_vals, embedder, fig_width, fig_height, text_size, title, mapping = None):
    embedding1 = embedder.encode(col1_unique_vals)
    embedding2 = embedder.encode(col2_unique_vals)

    reducer = umap.UMAP()
    embeddings_2d = reducer.fit_transform(np.vstack([embedding1, embedding2]))

    df = pd.DataFrame(data = {
        'x' : embeddings_2d[:,0],
        'y' : embeddings_2d[:,1],
        'cat' : ['curated']*embedding1.shape[0] + ['new']*embedding2.shape[0],
        'col': list(col1_unique_vals) + list(col2_unique_vals)
    })

    # make the base figure
    plt.figure(figsize = (fig_width, fig_height))
    # make the umap
    sns.scatterplot(df, x = 'x', y = 'y', hue = 'cat')
    # add the annotations for the points
    for i in range(len(df)):
        plt.text(x = embeddings_2d[i, 0], y = embeddings_2d[i, 1], s = df['col'][i], ha = 'right', fontsize = text_size)
    
    # if we also want to show lines between mapped columns
    if mapping != None:
        # loop through each entry in the mapping, and draw the corresponding line
        for key in mapping:
            value = mapping[key]
            x1, y1 = embeddings_2d[list(col1_unique_vals).index(key), :]
            x2, y2 = embeddings_2d[len(col1_unique_vals) + list(col2_unique_vals).index(value), :]
            plt.plot([x1, x2], [y1, y2], color = 'black', linestyle = 'dashed')
    plt.title(title)
    plt.show()
    # clear the figure, so that the legends start from nothing next time we make the figure
    plt.clf() 

# function to make the heatmap to visualize the columns' embeddings of two dataframes
def ColumnsHeatmap(curated_md, new_md, embedder, fig_width, fig_height):
    # get the distances values for the heatmap
    distances = GetDistanceBetweenSentences(curated_md.columns, new_md.columns, embedder)
    # make the df with the information for the heatmap
    df = pd.DataFrame(data = distances, columns = new_md.columns, index = curated_md.columns)
    # make the plot
    plt.figure(figsize=(fig_width, fig_height))
    sns.heatmap(df)
    plt.show()
    plt.clf()