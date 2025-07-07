from dotenv import load_dotenv
from langgraph.graph import StateGraph,END,add_messages
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
)

chat_prompt_template = ChatPromptTemplate.from_messages(messages=
    [
        ("system", """You are a viral linkedin influencer tasked to create viral linkedin posts on given topics.
        topic: {topic}""")
    ]
)
class AgentState(TypedDict):
    messages: Annotated[list,add_messages] = [(SystemMessage(content=f"You are a viral linkedin influencer tasked to create viral linkedin posts on given topics."))]

def llm_node(state: AgentState):
    return {"messages":[llm.invoke(state["messages"])]}

def post(state: AgentState):
    print(f"""\n{state["messages"][-1]}
          \n\n
          successfully posted on linkedin""")

    return {"messages":[AIMessage(content="posted on linkedin!")]}

def permit_post(state:AgentState):
    print(f"linkedin post:\n {state["messages"][-1].content}")

    if input("Permit agent to post on linkedin(y/n): ")=="y":
        return "post"
    else:
        return "collect_feedback"
def collect_feedback(state: AgentState):
    feedback = input("what else do you want: ")
    return {"messages":[HumanMessage(content=feedback)]}

graph = StateGraph(AgentState)

graph.add_node("llm_node",llm_node)
graph.add_node("post",post)
graph.add_node('collect_feedback',collect_feedback)

graph.add_edge("post",END)
graph.add_edge("collect_feedback","llm_node")
graph.add_conditional_edges("llm_node",permit_post,{"post":"post","collect_feedback":"collect_feedback"})

graph.set_entry_point("llm_node")
app = graph.compile()

result = app.invoke({
        "messages": [HumanMessage(content="how furious agentic AI is gonna dominate future")]
    })
