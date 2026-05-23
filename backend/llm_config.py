from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

import os


load_dotenv()


# CENTRALIZED LLM CONFIGURATION

llm = ChatOpenAI(

    model="gpt-3.5-turbo",

    temperature=0
)