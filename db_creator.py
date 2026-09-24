from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os 
import pandas as pd

dataframe = pd.read_csv('Merged_sorted_converted.csv')
if dataframe.empty == False:
    print('bugcheck456')
#check whether the file is empty or not 

embeddings = OllamaEmbeddings(model='mxbai-embed-large')
database_location = './chroma_langchain_database'
add_documents = not os.path.exists(database_location)

if add_documents:
    documents = []
    ids = []

    for index, row in dataframe.iterrows():
        document = Document(
            page_content='' + '' + f"{row['sender']}: {row['text']}",
            metadata = {'date': row['date'], 'time': row['time']},
            id = str(index)
        )
        ids.append(str(index))
        documents.append(document)

vector_store = Chroma(
    collection_name='gf_chat',
    persist_directory=database_location,
    embedding_function=embeddings
)

if add_documents:
    #vector_store.add_documents(documents=documents, ids=ids)
    #batch = 100
    #for i in range(0, len(documents), batch):
        #vector_store.add_documents(
            #documents=documents[i:i + batch],
            #ids=ids[i:i + batch]
        #)
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 10}
    )

