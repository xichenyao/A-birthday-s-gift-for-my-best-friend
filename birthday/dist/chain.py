import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from template import BASIC_TEMPLATE

def generate_response(memory, question, model_type="百川"):
    if model_type == "百川":
        llm = ChatOpenAI(
            openai_api_key="---",
            base_url="---",
            model="Baichuan3-Turbo",
        )
    elif model_type == "智谱":
        llm = ChatOpenAI(
            openai_api_key="---",
            base_url="---",
            model="glm-4",
        )
    elif model_type == "你自己的选择":
        llm = ChatOpenAI(
            openai_api_key=st.session_state.model_api_keys["你自己的选择"],
            base_url=st.session_state.model_urls["你自己的选择"],
            model=st.session_state.model_names["你自己的选择"],
        )
    else:
        raise ValueError(f"未知的模型类型: {model_type}")

    prompt = PromptTemplate.from_template(BASIC_TEMPLATE)
    
    # Use the prompt to create a chain
    inputs = question
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )

    # Generate the response
    response = chain.invoke(inputs)
    return response
