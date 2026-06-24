from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.web_search import web_search
from tools.web_scraper import web_scrape

from dotenv import load_dotenv
load_dotenv()


#  Model Setup

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
)
