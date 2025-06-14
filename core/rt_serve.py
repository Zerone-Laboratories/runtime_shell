from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
)
from typing import List


class RAG:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["runtime_db"]
        self.collection = self.db["runtime_instruct"]

        self.documents = []
        for doc in self.collection.find({}):
            self.documents.append(doc["instructions"])

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.splitted_docs = self.text_splitter.create_documents(self.documents)

        self.vectorstore = Chroma(collection_name="runtime_collection", embedding_function=GPT4AllEmbeddings())

        self.vectorstore.reset_collection()
        self.vectorstore.add_documents(self.splitted_docs)


    def search_runtime_docs(self, query, top_k=3):
        results = self.vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in results]




class runtimeEngine:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None
        )
        self.rag = RAG()
        self.client = MultiServerMCPClient(
            {
                "rigel tools": {
                    "url": "http://localhost:8001/sse",
                    "transport": "sse",
                }
            },
        )
        self.model = ChatGroq(model="llama3-70b-8192")
        self.tools = None
        self.agent = None
        self._initialized = False
        # Default Mode: Shell
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

        search_results = self.rag.search_runtime_docs("Shell mode, program")
        retrieved_context = "\n".join(search_results)

        self.system_instruction = f"{retrieved_context}"

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_instruction),
            ("assistant", "{history}"),
            ("human", "{input} Always `import os` Don't  ever give comments"),
        ])
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=False
        )

    def predict(self, input):
        return self.conversation.run(input=input)
    
    async def initialize(self):
        if not self._initialized:
            try:
                self.tools = await self.client.get_tools()
                self.agent = create_react_agent(self.model, self.tools)
                self._initialized = True
            except Exception as e:
                print(f"Failed to initialize MCP client: {e}")
                raise e

    async def mcp_call(self, input_text: str, RAG: bool = False) -> str:
        try:
            if not self._initialized:
                await self.initialize()
            chat_history = self.memory.chat_memory.messages

            if RAG:
                search_results = self.rag.search_runtime_docs(input_text)
                retrieved_context = "\n".join(search_results)
                system_msg = SystemMessage(content=f"{self.system_instruction}\n\nAdditional Context:\n{retrieved_context}")
            else:
                system_msg = SystemMessage(content=self.system_instruction)

            # messages = [system_msg] + chat_history + [HumanMessage(content=input_text)]
            messages = [HumanMessage(content=input_text)]
            result = await self.agent.ainvoke({"messages": messages})
            ai_response = result["messages"][-1]
            self.memory.chat_memory.add_user_message(input_text)
            self.memory.chat_memory.add_ai_message(ai_response.content)

            return ai_response.content
        except Exception as e:
            # Log the error and re-raise it so the calling function can handle it
            print(f"Error in mcp_call: {e}")
            raise e


if __name__ == "__main__":
    runtime = runtimeEngine()
    query = "check my CPU temperatures"
    print(runtime.predict(input=query))
    query = "show it in a table"
    print(runtime.predict(input=query))
