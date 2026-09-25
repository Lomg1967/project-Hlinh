from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import csv
import math
import pandas as pd
from pathlib import Path


csv_directory = Path(__file__).resolve().parent / 'db_csv'
embedding_batch_size = 50
PRINT_SKIPPING_COMPLETED_CHUNKS = False

embeddings = OllamaEmbeddings(model='mxbai-embed-large')
database_location = './chroma_langchain_database'

vector_store = Chroma(
    collection_name='gf_chat',
    persist_directory=database_location,
    embedding_function=embeddings,
)

for csv_file in sorted(csv_directory.glob('*.csv')):
    try:
        with csv_file.open('r', encoding='utf-8-sig', newline='') as file:
            row_count = max(sum(1 for row in csv.reader(file)) - 1, 0)

        if row_count == 0:
            print(f'{csv_file.name} is empty')
            continue

        chunk_size = max(math.ceil(row_count / 5), 1)
        chunks = pd.read_csv(csv_file, chunksize=chunk_size)

        for chunk_number, dataframe in enumerate(chunks, start=1):
            documents = []
            ids = []

            for index, row in dataframe.iterrows():
                row_values = {
                    str(column): str(value)
                    for column, value in row.items()
                    if pd.notna(value)
                }
                page_content = '\n'.join(
                    f'{column}: {value}' for column, value in row_values.items()
                )
                metadata = row_values.copy()
                metadata['source'] = csv_file.name

                document = Document(
                    page_content=page_content,
                    metadata=metadata,
                    id=f'{csv_file.name}:{index}',
                )
                ids.append(document.id)
                documents.append(document)

            existing_ids = set(vector_store.get(ids=ids).get('ids', []))
            pending_documents = [
                document for document in documents if document.id not in existing_ids
            ]

            if not pending_documents:
                if PRINT_SKIPPING_COMPLETED_CHUNKS:
                    print(
                        f'Skipping completed chunk {chunk_number} of {csv_file.name} '
                        f'({len(dataframe)} rows)'
                    )
                continue

            for batch_start in range(0, len(pending_documents), embedding_batch_size):
                batch_documents = pending_documents[
                    batch_start:batch_start + embedding_batch_size
                ]
                batch_ids = [document.id for document in batch_documents]
                vector_store.add_documents(
                    documents=batch_documents,
                    ids=batch_ids,
                )
                print(
                    f'Embedded chunk {chunk_number} of {csv_file.name}: '
                    f'{batch_start + len(batch_documents)}/{len(pending_documents)} rows'
                )
    except pd.errors.EmptyDataError:
        print(f'{csv_file.name} is empty, pd.read_csv failed')
        continue

retriever = vector_store.as_retriever(
    search_kwargs={"k": 10}
)
