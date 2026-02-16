"""
This is a simple chatbot that uses the OpenAI API to generate responses.
"""
import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI


load_dotenv()

# Create an instance of ChatOpenAI
chat = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",  # Choose a compact but powerful model
    temperature=0.7,  # Balanced creativity setting
    max_tokens=50,  # Keep responses concise
    top_p=0.9,  # Consider 90% of probability mass
    frequency_penalty=0.5,  # Discourage repetition
    presence_penalty=0.3,  # Gently encourage new topics
)

messages = [SystemMessage(content="You are a tour guide")]


# Create a function to send a message and update conversation history
def send_message(user_input):
    # Add the user's message to the conversation
    messages.append(HumanMessage(content=user_input))
    # Get the AI's response
    response = chat.invoke(messages)
    # Add the AI's response to the conversation history
    messages.append(AIMessage(content=response.content))
    # Return the AI's response
    return response.content

