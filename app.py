import numpy as np
import pandas as pd
import wikipediaapi
from functions import process_page, split_text_into_chunks

# Call the Wikipedia function through a user_agent and specify the language
# Call the Wikipedia function through a user_agent and specify the language
string = "SemSearchDemo/2.0 (Jasper B)"
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en')


# Iterating over all page titles to create the final df with individual chunks

page_titles = ["The Shawshank Redemption", "The Dark Knight", "Pulp Fiction", "The Godfather", "Goodfellas"]

all_dfs = []

for title in page_titles:
    df = process_page(title)
    if df is not None:
        all_dfs.append(df)

fixed_chunk_df = pd.concat(all_dfs, ignore_index=True)
fixed_chunk_df