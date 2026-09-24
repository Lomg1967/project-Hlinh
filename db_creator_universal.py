from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os 
import pandas as pd
from pathlib import Path


cvsfiles = Path(f'D:\project Hlinh\db_csv')

for file in cvsfiles:
    check = cvsfiles.iterdir(file)
    if check.glob('*.csv'):
        dataframe = pd.read_csv(file)
        if dataframe.empty == True:
            print(f'{file} is empty')


for file in cvsfiles.glob('*.csv'):
        dataframe = pd.read_csv(file)

embeddings = OllamaEmbeddings(model='mxbai-embed-large')
database_location = './chroma_langchain_database'
add_documents = not os.path.exists(database_location)