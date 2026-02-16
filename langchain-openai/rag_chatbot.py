from document_processor import DocumentProcessor
from chat_engine import ChatEngine

class RAGChatbot:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.chat_engine = ChatEngine()
        
    def upload_document(self, file_path):
        """Upload and process a document"""
        try:
            self.document_processor.process_document(file_path)
            return "Document successfully processed."
        except ValueError as e:
            return f"Error: {str(e)}"    
        
    def reset_documents(self):
        """Reset the document processor"""
        self.document_processor.reset()
        return "Document knowledge has been reset."    
    
    def send_message(self, message):
        """Send a message to the chatbot and get a response"""
        # Retrieve relevant document chunks based on the user's query
        relevant_docs = self.document_processor.retrieve_relevant_context(message)

        # Initialize an empty string for the context
        context = ""

        # Loop through each relevant document
        for doc in relevant_docs:
            # Extract the source from metadata, defaulting to 'unknown' if not available
            source = doc.metadata.get('source', 'unknown')
            # Extract the content of the document
            content = doc.page_content
            # Append the source and content to the context string
            context += f"Source: {source}\n{content}\n\n"

        # Send the user's message along with the context to the chat engine
        return self.chat_engine.send_message(message, context)   
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_engine.reset_conversation()
        return "Conversation history has been reset." 
    
    def reset_all(self):
        """Reset both conversation and documents"""
        self.reset_conversation()
        self.reset_documents()
        return "Both conversation history and document knowledge have been reset."
    
    
if __name__ == "__main__":
    # Initialize the RAG chatbot
    chatbot = RAGChatbot()

    # Upload a document
    result = chatbot.upload_document("data/document.pdf")
    print(result)

    # Send a message about the document
    query = "My 3yo is so stubborn. How can I handle the situation?"
    response = chatbot.send_message(query)
    print(f"\nQuestion: {query}")
    print(f"Answer: {response}")    
    
    # Reset everything
    result = chatbot.reset_all()
    print(result)

    # Try asking about Sherlock Holmes
    final_query = "Tell me about Sherlock Holmes."
    response = chatbot.send_message(final_query)
    print(f"\nQuestion: {final_query}")
    print(f"Answer: {response}")