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




def web_search_agent():
    """Agent that searches the web for recent information."""
    return create_agent(
        model=llm,
        tools=[web_search],
    )


def web_reader_agent():
    """Agent that scrapes and reads web pages in depth."""
    return create_agent(
        model=llm,
        tools=[web_scrape],
    )
