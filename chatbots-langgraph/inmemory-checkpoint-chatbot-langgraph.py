from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,END,add_messages
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
)
memory = MemorySaver()

class BasicState(TypedDict):
    messages: Annotated[list,add_messages]
def llm_node(state: BasicState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }
graph = StateGraph(BasicState)
graph.add_node("llm_node",llm_node)
graph.add_edge("llm_node",END)
graph.set_entry_point("llm_node")
app = graph.compile(checkpointer=memory)
config = { "configurable":{
   "thread_id":1
}
}

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = app.invoke({"messages":[HumanMessage(user_input)]},config=config)
    print(f"Bot: {response["messages"][-1].content}")
