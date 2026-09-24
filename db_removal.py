##
## ONLY RUN THIS FILE IF YOU WANT TO REMOVE THE DATABASE
## THIS WILL REMOVE ALL THE DATA STORED IN THE DATABASE
##

import shutil
import os

DATABASE_LOCATION = "./chroma_langchain_database"

try:
    if os.path.exists(DATABASE_LOCATION):
        shutil.rmtree(DATABASE_LOCATION)
        print("Chroma database removed.")
    else:
        print("Folder does not exist.")
except Exception as e:
    print(f"Error: {e}")