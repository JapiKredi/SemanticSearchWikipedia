<b>Semantic Search Wikipedia</b>
We will implement those concepts to build a semantic search system using Wikipedia data. 
We will then explore vector stores that are specifically designed to store and retrieve vector embeddings. 
Once you understand the concepts of vector databases, we will augment the semantic search application using a popular vector store - ChromaDB.

The <b> encoding pipeline</b>  deals with ingesting the documents for search, generating the vector embeddings and then storing them for later retrieval. 
The pipeline consists of the following steps:
1: Collecting documents for embedding
2: Creating text embeddings to encode semantic information
3: Storing embeddings in a database for later retrieval upon receiving a query
 
Once the embeddings are generated, you can store them locally for later retrieval through the search or decoding pipeline. 
The search or <b>decoding pipeline</b> compares the vector embeddings of the query against the vector embeddings contained within the document. It generally consists of the following steps:
Retrieving the user’s query
1: Comparing the embeddings of the query and the document embeddings generated from the encoding pipeline
2: Retrieving the relevant candidate documents using an appropriate distance metric
3: Returning the final search results

The data we will primarily work on for this demonstration is the Wikipedia articles data for specific movies, which will be extracted using the wikipedia-api library in Python. 
Once the text is extracted, the next step is to perform chunking. 
In the previous module, we discussed the various chunking strategies for documents, such as fixed-size chunking, natural delimiter, max-token window and overlapping window chunking strategies.

In this code, I am  demonstrating how to perform fixed window chunking on the Wikipedia text. 
<b>Fixed-size chunking</b> is a common and straightforward approach to chunking, where the number of tokens in each chunk is predetermined.
