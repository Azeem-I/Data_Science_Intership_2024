from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st 

st.title("RAG based Google Assistant")
st.header("Ask me Anything About Infinite Context Length Paper")

##loading the documents stored as pdf 
loader = PyPDFLoader(r"D:\edu\INNO\LangChain_Projects\paper_infinite_context_length.pdf")
data = loader.load_and_split() 

# Split the document into chunks

from langchain_text_splitters import NLTKTextSplitter

text_splitter = NLTKTextSplitter(chunk_size=500, chunk_overlap=100)

chunks = text_splitter.split_documents(data)



##loading the file 
f=open(r"D:\edu\INNO\LangChain_Projects\gemini_key.txt")
key=f.read() 
## creating chat model
chat_model=ChatGoogleGenerativeAI(google_api_key=key,model="gemini-1.5-pro-latest") 



###creating embeddings 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
embedding_model=GoogleGenerativeAIEmbeddings(google_api_key=key,model="models/embedding-001")

##store the chunks in vector store 
from langchain_community.vectorstores import Chroma 



##embedd each page and load it into the vector store 
db=Chroma.from_documents(chunks,embedding_model,persist_directory="/Chroma_db_1")

##persist the databaseon the drive 
db.persist()  

##setting aconnection with the chroma 
db_connection=Chroma(persist_directory="/Chroma_db_1",embedding_function=embedding_model)

###converting chromadb cnnection to retriever object 
retriever=db_connection.as_retriever(search_kwargs={"k":10}) 

user_input=st.text_input("Enter your query ")

retrieved_docs=retriever.invoke(user_input)

chat_template=ChatPromptTemplate.from_messages([
    #system message prompt template 
    SystemMessage(content="""You are a helpful AI assistant.You take the context and and question from the user and give response based on context""")
    ,#Human message prompt template 
    HumanMessagePromptTemplate.from_template("""Answer the question beased on given context.
                   Context:{Context}
                   Question:{question}
                Answer  """),
                ]) 

#############
output_parser=StrOutputParser()
###########
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

############
rag_chain=(
    {"Context":retriever | format_docs,"question":RunnablePassthrough()}
    | chat_template
    | chat_model
    | output_parser 
)

##invoking
response=rag_chain.invoke(user_input)
st.write(response)

