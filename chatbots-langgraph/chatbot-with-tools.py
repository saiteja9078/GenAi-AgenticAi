from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,END,add_messages
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
)
search_tool = TavilySearchResults(max_results=4)
llm_with_tools = llm.bind_tools([search_tool])
print(llm_with_tools.invoke("get the weather in San Francisco live"))
class BasicState(TypedDict):
    messages: Annotated[list,add_messages]
def llm_node(state: BasicState):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }
def conditional_edge(state: BasicState):
 return "tool_node" if hasattr(state["messages"][-1],"tool_calls") and len(state["messages"][-1].tool_calls)>0 else END

tool_node = ToolNode([search_tool],messages_key="messages")
graph = StateGraph(BasicState)
graph.add_node("llm_node",llm_node)
graph.add_node("tool_node",tool_node)
graph.add_conditional_edges("llm_node",conditional_edge,{"tool_node":"tool_node",END:END})
graph.add_edge("tool_node","llm_node")
graph.set_entry_point("llm_node")
app = graph.compile()
print(app.invoke({"messages":[HumanMessage("What is the weather in San Francisco?")]}))
