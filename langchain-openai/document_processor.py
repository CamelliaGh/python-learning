from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class DocumentProcessor:
    """Processes a document and returns a vector store"""
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 100
        self.embedding_model = OpenAIEmbeddings()
        self.vectorstore = None
        
    def load_document(self, file_path):
        """Load a document based on its file type"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file format")           
        return loader.load()  
    
    def process_document(self, file_path):
        """Process a document and add it to the vector store"""
        # Load the document
        docs = self.load_document(file_path)
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
        split_docs = text_splitter.split_documents(docs)
        
        # Create or update the vector store
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding_model)
        else:
            self.vectorstore.add_documents(split_docs)
            
    def retrieve_relevant_context(self, query, k=3):
        """Retrieve relevant document chunks for a query"""
        if self.vectorstore is None:
            return []
            
        return self.vectorstore.similarity_search(query, k=k)      
    
    def reset(self):
        """Reset the document processor"""
        self.vectorstore = None  