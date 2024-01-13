import numpy as np
import pandas as pd
import wikipediaapi
from functions import process_page, split_text_into_chunks

# Call the Wikipedia function through a user_agent and specify the language
# Call the Wikipedia function through a user_agent and specify the language
string = "SemSearchDemo/2.0 (Jasper B)"
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en')

# Function to extract and store Wikipedia page information

def process_page(page_title):

    page = wiki_wiki.page(page_title)

    if page.exists():
        page_text = page.text
        chunk_size = 1000  # Set your desired chunk size (in characters)

        text_chunks = split_text_into_chunks(page_text, chunk_size)

        # Create a DataFrame to store the chunks and page title
        data = {'Title': [], 'Chunk Text': []}

        for idx, chunk in enumerate(text_chunks):
            data['Title'].append(page_title)
            data['Chunk Text'].append(chunk)

        return pd.DataFrame(data)

    else:
        print(f"The page '{page_title}' does not exist on Wikipedia.")
        return None
    
# Function to split text into fixed-size chunks

def split_text_into_chunks(text, chunk_size):
    chunks = []
    words = text.split()  # Split the text into words

    current_chunk = []  # Store words for the current chunk
    current_chunk_word_count = 0  # Count of words in the current chunk

    for word in words:
        if current_chunk_word_count + len(word) + 1 <= chunk_size:
            current_chunk.append(word)
            current_chunk_word_count += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_chunk_word_count = len(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# Iterating over all page titles to create the final df with individual chunks

page_titles = ["The Shawshank Redemption", "The Dark Knight", "Pulp Fiction", "The Godfather", "Goodfellas"]

all_dfs = []

for title in page_titles:
    df = process_page(title)
    if df is not None:
        all_dfs.append(df)

fixed_chunk_df = pd.concat(all_dfs, ignore_index=True)
fixed_chunk_df