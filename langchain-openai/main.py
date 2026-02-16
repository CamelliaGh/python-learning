from document_processor import DocumentProcessor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize the document processor
processor = DocumentProcessor()

# Process a document
file_path = "data/a_scandal_in_bohemia.pdf"
processor.process_document(file_path)

# Initialize the chat model
chat = ChatOpenAI()

# Define a query
query = "What is the main mystery in the story?"

# Retrieve relevant context
relevant_docs = processor.retrieve_relevant_context(query)
context = "\n\n".join([doc.page_content for doc in relevant_docs])

# Create a prompt template for RAG
prompt_template = ChatPromptTemplate.from_template(
    "Answer the following question based on the provided context.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)

# Format the prompt with our context and query
prompt = prompt_template.format(context=context, question=query)

# Get the response from the model
response = chat.invoke(prompt)

# Print the question and the AI's answer
print(f"Question: {query}")
print(f"Answer: {response.content}")