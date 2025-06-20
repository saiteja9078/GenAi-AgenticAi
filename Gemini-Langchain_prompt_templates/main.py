#Integrate with gemini api

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import streamlit as st
import warnings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory



st.title("LangChain with Gemini API")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0394832619-e64baf946f3b.json"


input_text = st.text_input("Search the topic you want")

# Memory

topic_memory = ConversationBufferMemory(input_key='input_text', memory_key='chat_history')
summary_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
question_memory = ConversationBufferMemory(input_key='quiz_question', memory_key='description_history')

# Prompt 1: Summarize the input topic
prompt_temp1 = PromptTemplate(
    input_variables=["input_text"],
    template="Give a concise summary of the topic: {input_text}. Keep it simple and under 3 sentences.",
)
#Gemini initialisation
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))


chain1 = LLMChain(
    llm=llm,
    prompt=prompt_temp1,
    verbose=True,
    output_key="summary",
    memory=topic_memory
)

prompt_temp2 = PromptTemplate(
    input_variables=["summary"],
    template="Based on this summary: {summary}, create a challenging multiple-choice question with 4 options dont give answer",
)

chain2 = LLMChain(
    llm=llm,
    prompt=prompt_temp2,
    verbose=True,
    output_key="quiz_question",
    memory=summary_memory
)

prompt_temp3 = PromptTemplate(
    input_variables=["quiz_question"],
    template="answer this \n {quiz_question}",
)
chain3 = LLMChain(
    llm=llm,
    prompt=prompt_temp3,
    verbose=True,
    output_key="quiz_answer",
    memory=question_memory
)

#remembers only previos context
# parent_chain = SimpleSequentialChain(
#     chains=[chain1,chain2],
#     verbose=True
# 

#remembers whole conversational context

parent_chain = SequentialChain(
    chains=[chain1, chain2,chain3],
    input_variables=["input_text"],
    output_variables=["summary", "quiz_question", "quiz_answer"]
)
if input_text:
    st.write(parent_chain({'input_text':input_text}))
    with st.expander('Topic Name'): 
        st.info(topic_memory.buffer)

    with st.expander('Question and answering'): 
        st.info(question_memory.buffer)
