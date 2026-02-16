import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI




load_dotenv()



# Define the file path to our Sherlock Holmes story
FILE_PATH = "data/document.pdf"

# Create a PDF loader for our document
pdf_loader = PyPDFLoader(FILE_PATH)

# Load the document
docs = pdf_loader.load()


# Print the number of document chunks loaded
# print(f"Loaded {len(docs)} document chunks")

# Print the content of the first chunk
# print(f"\nFirst 200 characters of the first chunk:\n{docs[0].page_content[:200]}")

# Print the metadata of the first chunk
# print(f"\nMetadata of the first chunk:\n{docs[0].metadata}")


# Initialize the text splitter with a specified chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = text_splitter.split_documents(docs)
# Print the number of chunks after splitting

# Print the content of the first chunk
print(f"\nFirst chunk content:\n{split_docs[0].page_content}")

# Initialize the OpenAI embedding model
embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize OpenAIEmbeddings with custom parameters
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",  # Choose which embedding model to use
    dimensions=1536,  # How detailed you want your vectors to be
    chunk_size=1000,  # How many pieces of text to process at once
)

# Extract the text content from our first document chunk
document_text = split_docs[0].page_content

# Generate the embedding vector for this text
embedding_vector = embedding_model.embed_query(document_text)

vectorstore = FAISS.from_documents(split_docs, embedding_model)


QUERY = "What's an effective way to address kicking, hitting and pinching?"

# Perform similarity search to find the top 3 most relevant document chunks
retrieved_docs = vectorstore.similarity_search(QUERY, k=3)
print(f"len:{len(retrieved_docs)}")

# Loop through each retrieved document
for doc in retrieved_docs:
    # Print the first 300 characters of each document chunk
    print(doc.page_content[:300], "...\n")


# Create a prompt template for RAG
prompt_template = ChatPromptTemplate.from_template(
    "Answer the following question based on the provided context.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)

CONTEXT = "\n\n".join([doc.page_content for doc in retrieved_docs])


PROMPT = prompt_template.format(context=CONTEXT, question=QUERY)


chat = ChatOpenAI()
response = chat.invoke(PROMPT)
# Print the question and the AI's answer
print(f"Question: {QUERY}")
print(f"Answer: {response.content}")