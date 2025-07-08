from dotenv import load_dotenv
from langgraph.graph import StateGraph,END,add_messages,START
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage,HumanMessage 
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langgraph.types import Command,interrupt
from langgraph.checkpoint.memory import MemorySaver

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
    linkedin_topic : Annotated[str,add_messages]
    messages: Annotated[list,add_messages] = [].append(SystemMessage(content=f"You are a viral linkedin influencer tasked to create viral linkedin posts on given topics."))
    feedback: Annotated[list[str],add_messages]

def llm_node(state: AgentState):
    feedback =state["feedback"] if state["feedback"] else "no feedback yet"
    prompt = f"""
        Linkedin topic: {state["linkedin_topic"]}
        Human Feedback: {feedback[-1]}
        generate a strcutured and well writtin linkedin post
        consider human feedback to refine the promise
"""
    resposne = llm.invoke(prompt)
    print("ai generated linkedin content:\n")
    print(resposne.content)

    return Command(
        goto="human_node",
        update={
            "messages":[AIMessage(content=resposne.content)]
        }
    )


def post(state: AgentState):
    print(f"""\n{state["messages"][-1]}
          \n\n
          successfully posted on linkedin""")

    return Command(goto=END,
                   update={"messages":[AIMessage(content="posted on linkedin!")]})

def human_node(state: AgentState):
    feedback = interrupt("\nApproval to post(y/n):")

    if feedback=="done":
        return Command(goto="post",update={"messages":[AIMessage(content="finalized post!")]})
    else:
        return Command(goto="llm_node",update={
            "feedback":[HumanMessage(content=feedback)]
        })
graph = StateGraph(AgentState)
checkpointer = MemorySaver()
thread_config = {
    "configurable":{
        "thread_id":4972
    }
}
graph.add_node("llm_node",llm_node)
graph.add_node("post",post)
graph.add_node('human_node',human_node)

graph.add_edge(START,"llm_node")

graph.set_entry_point("llm_node")
app = graph.compile(checkpointer=checkpointer)

topic = "write a linkedin post on how agentic ai gonna take the future"
initial_state = {
    "linkedin_topic":topic,
    "messages":[]
    ,"human_feedback":[]
}
for chunk in app.stream(initial_state,config=thread_config):
    for node_id,value in chunk.items():
        if(node_id=="__interrupt__"):
            while True:
                user_feedback = input("\nprovide feedback (or type done): ")
                
                app.invoke(Command(resume=user_feedback),config=thread_config)

                if user_feedback.lower()=="done":
                    break