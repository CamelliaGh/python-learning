import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()

class ChatEngine:
    
    def __init__(self):
        self.chat_model = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_message = (
            "You are a helpful assistant that ONLY answers questions based on the "
            "provided context. If no relevant context is provided, do NOT answer the "
            "question and politely inform the user that you don't have the necessary "
            "information to answer their question accurately."
        )

        # Define the prompt template with explicit system and human messages
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_message),
                HumanMessagePromptTemplate.from_template(
                    "Context:\n{context}\n\nQuestion: {question}"
                ),
            ]
        )
        
        # Optionally, keep conversation history for display/logging only
        self.conversation_history = []

    def send_message(self, user_message, context=""):
        """Send a message to the chat engine and get a response"""
        # Format the messages using the prompt template (includes system message)
        messages = self.prompt.format_messages(context=context, question=user_message)
        # Get the response from the model
        response = self.chat_model.invoke(messages)

        # Optionally, track the conversation for display/logging
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=response.content))

        # Return the AI's response content
        return response.content

    def reset_conversation(self):
        """Reset the conversation history (for display/logging only)"""
        self.conversation_history = []


if __name__ == "__main__":
    chat_engine = ChatEngine()

    # Send a message without context (should politely decline)
    query = "What is the capital of France?"
    response = chat_engine.send_message(query)
    print(f"Question: {query}")
    print(f"Answer: {response}")

    # Print conversation history
    print("\nConversation history:")
    print(chat_engine.conversation_history)
    
    
    
    # Send a message with context (should answer using only the context)
    context = """Paris is the capital and most populous city of France. 
    The Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral are among its most famous landmarks."""
    query = "Tell me about the landmarks mentioned."

    # Get response with context provided
    response = chat_engine.send_message(query, context)

    # Display the question and answer
    print(f"\nQuestion with context: {query}")
    print(f"Answer: {response}")

    # Print updated conversation history
    print("\nUpdated conversation history:")
    print(chat_engine.conversation_history)
    
    # Reset the conversation history (for display/logging only)
    chat_engine.reset_conversation()
    print("\nConversation history has been reset.")

    # Print conversation history after reset
    print("\nConversation history after reset:")
    print(chat_engine.conversation_history)
