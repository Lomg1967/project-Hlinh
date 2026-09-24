from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from db_creator import retriever

print('bugcheck123')

model = OllamaLLM(model='artifish/llama3.2-uncensored')

template = '''
You are my girlfriend.
You are very kind, caring, and loving. 
You are also very smart and funny. 
You are always there for me when I need you. 



This is our conversation history: {conversation_history}

let's start our conversation: {conversation}

'''
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    conversation = input('>>> ')
    if conversation == 'q':
        break

    conversation_history = retriever.invoke(conversation)

    result = chain.invoke({'conversation': conversation,
                           'conversation_history': conversation_history})
    print(result)