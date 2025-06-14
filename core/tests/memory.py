# Settling to ConversationBufferMemory, because this is a tool and user will not 
# chat with it per se.

import time
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate\

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None
)

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    verbose=False,
    memory=memory
)

conversation.predict(input="Hi there !, I am sam")

conversation.predict(input="How are you doing today ?")
time.sleep(1)
conversation.predict(input="What is your name ?")
conversation.predict(input="Say bye")

print(conversation.memory.buffer)