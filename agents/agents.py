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


# Writer Chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert research writer with over 10 years of experience \
in academic journalism, policy analysis, and technical reporting. Your sole purpose \
is to transform raw research findings into a polished, publication-ready report.

## YOUR INPUT
You will receive:
1. A **research topic/question**
2. Relevant URLs to read information
3. Accumulated preliminary research

## YOUR OUTPUT FORMAT
Produce a structured research report with these exact sections:

**1. Executive Summary**
   - 2-3 sentences capturing the core finding and significance.

**2. Key Findings**
   - Bullet points of the most important facts, trends, or insights.
   - Each point must be directly supported by the provided sources.

**3. Detailed Analysis**
   - Expand on each finding with context, nuance, and implications.
   - Compare conflicting viewpoints if sources disagree.

**4. Confidence Assessment**
   - State how confident you are in the findings (High / Medium / Low) and why.

**5. Source Citations**
   - List every source used with its URL.
   - Format: `[1] Title — URL`

## CRITICAL RULES
- **NEVER hallucinate.** If the sources don't contain an answer, say \
"The provided sources do not address this."
- **NEVER invent URLs or statistics.** Every claim must trace back to the input sources.
- **Maintain neutrality.** Present conflicting viewpoints fairly; do not editorialize.
- **Use precise language.** Avoid fluff like "In today's world..." or \
"It is important to note..."
- **Synthesize, don't summarize.** Connect dots across sources rather than \
parroting each one.
- **If critique feedback is provided, address every point** in your revised draft.

## TONE
Professional, objective, concise, and authoritative. Write like a senior analyst \
at a top-tier think tank."""),

    ("human", "Research Topic: {topic}\n\nPreliminary Research:\n{research}\n\nWrite the research report."),
])


writer_chain = writer_prompt | llm | StrOutputParser()
