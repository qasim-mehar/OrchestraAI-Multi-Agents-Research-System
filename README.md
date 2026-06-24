# OrchestraAI

**A multi-agent research system built to understand how modern AI pipelines actually work.**

This is not a wrapper around a chatbot. OrchestraAI is a pipeline of specialized AI agents  each with a distinct role  coordinated to produce a peer-reviewed research report on any topic you give it. One agent searches the web. Another reads and extracts content from sources. A third synthesizes everything into a structured report. A fourth tears that report apart looking for flaws.

The project was built as a deep learning exercise in agent design, LLM orchestration, tool use, and prompt engineering. Every architectural decision was made intentionally, and this README explains why.

---

## What It Does

You give OrchestraAI a research question. It returns a full, structured research report with an attached critic review  all without you lifting a finger after the initial prompt.

```
topic? : Pakistan's mediation role in the Iran-US conflict?

  Stage 1   Web Search Agent searches for recent, reliable sources
  Stage 2   Web Reader Agent picks the best URL and scrapes it deeply
  Stage 3   Writer Chain synthesizes all findings into a formatted report
  Stage 4   Critic Chain peer-reviews the report and scores it out of 10
```

The output includes an executive summary, key findings, detailed analysis, a confidence assessment, and source citations  followed by an independent critique identifying exactly what the report got right and what it missed.

---

## What I Learned Building This

This project was built specifically to develop a real understanding of how multi-agent AI systems work  not just use them. Here is what I actually learned at each stage.

### Agent Design and Tool Use

An agent is an LLM that can decide, at runtime, which tools to call and in what order. LangChain's `create_react_agent` implements the ReAct pattern (Reason + Act): the model reasons about what it needs, picks a tool, observes the result, and reasons again.

Writing a `@tool` decorated function taught me that the docstring is not documentation  it **is** the tool's interface to the model. The LLM reads the docstring to decide when and how to call the function. A vague docstring produces wrong tool calls.

### LLM Chains vs Agents

Not everything should be an agent. Agents are powerful but expensive  they make multiple LLM calls per task. The Writer and Critic in this project are **chains** (a prompt template piped directly to an LLM and parser), not agents. They do not need tools; they just need to think. Knowing when to use a chain versus an agent is one of the most important judgment calls in system design.

### Prompt Engineering at Depth

The Writer and Critic prompts took more time than the code. I learned that a prompt is really a contract: you are specifying input format, output format, tone, constraints, and fallback behavior all at once. The CRITICAL RULES section in both prompts exists because without explicit anti-hallucination constraints, models invent plausible-sounding facts.

The Writer is instructed to synthesize across sources, not summarize them one by one. The Critic is instructed never to praise generically  every compliment must cite a specific sentence. These constraints came from observing bad output and iterating.

### Message Formats in LangChain

LangChain has two valid ways to pass messages to an agent: the tuple format `("human", "content")` or the dict format `{"role": "user", "content": "..."}`. Using `{"user": "content"}` (missing the `role` key) causes a `MESSAGE_COERCION_FAILURE` that is hard to debug if you do not know what to look for. I hit this bug and now I understand the message schema deeply.

### Pipeline State Management

The pipeline maintains a single `state` dict that accumulates outputs at each stage. This is intentional. In production systems, this would be a LangGraph `StateGraph` with typed state channels  but building the explicit dict version first made me understand *why* typed state matters: without it, a single key typo (`search_results` vs `basic_results`) silently breaks the whole pipeline.

### Model Orchestration

Different agents benefit from different models. The search agent needs speed and tool-calling reliability. The writer needs strong long-form generation. The critic needs careful reasoning. In a production system, you would route each agent to the model it is best suited for  not use one model for everything. Building this project made that tradeoff concrete rather than theoretical.

---

## Key Concepts Demonstrated

**ReAct Agent Pattern**  agents that reason before acting, observe results, then reason again before the next action.

**Tool-Augmented LLMs**  language models extended with callable functions (search, scrape) that give them access to real-time external information.

**LCEL (LangChain Expression Language)**  the pipe operator `|` that chains prompt templates, LLMs, and output parsers into composable pipelines.

**Multi-Stage Orchestration**  breaking a complex task into discrete stages, each handled by the agent or chain best suited for that job.

**Prompt Contracts**  structured system prompts that specify input/output format, constraints, and fallback behavior to produce reliable, consistent outputs.

---


## Architecture

```
User Input (topic)
      |
      v
 Web Search Agent          uses: Tavily Search API
      |
      v
 Web Reader Agent          uses: Web Scraper Tool
      |
      v
 Writer Chain              LLM + structured prompt
      |
      v
 Critic Chain              LLM + evaluation prompt
      |
      v
 Final Report + Critique
```

Each stage is independent. The agents do not share state directly  instead, the pipeline passes outputs explicitly between stages. This is a deliberate design choice: it makes the system easier to debug, test, and extend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangChain + LangGraph |
| LLM | Mistral Large (via Mistral AI API) |
| Web Search | Tavily Search API |
| Web Scraping | Custom scraper tool |
| Output Formatting | Rich (terminal) |
| Environment | Python 3.11+, uv |

---

## Project Structure

```
OrchestraAI/
  agents/
    agents.py          Agent factories, writer chain, critic chain
  tools/
    web_search.py      Tavily-powered search tool
    web_scraper.py     URL content extraction tool
  pipeline.py          Orchestration logic  runs the full pipeline
  .env                 API keys (not committed)
  pyproject.toml       Dependencies managed with uv
```

---

## Getting Started

**Prerequisites:** Python 3.11+, uv installed, API keys for Mistral AI and Tavily.

```bash
# Clone and enter the project
git clone https://github.com/qasim-mehar/OrchestraAI.git
cd OrchestraAI

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Add your MISTRAL_API_KEY and TAVILY_API_KEY to .env

# Run the pipeline
uv run pipeline.py
```

You will be prompted to enter a research topic. The pipeline runs all four stages automatically and prints the final report and critique to the terminal.

---

## Known Limitations

The pipeline runs sequentially. There is no parallelism  the web reader waits for the search agent to finish, the writer waits for the reader, and so on. A production version would use LangGraph's parallel node execution to run independent stages concurrently.

The pipeline runs once. There is no feedback loop: if the Critic scores the report below 7, the system does not automatically send the critique back to the Writer for a revised draft. Adding that loop is the natural next step.

Rate limits on free API tiers can cause intermittent failures on long topics that generate many tool calls. The system does not currently retry failed tool calls.

---

## Roadmap

- [ ] Convert pipeline to a LangGraph `StateGraph` with typed state channels
- [ ] Add revision loop: if Critic score is below 7, Writer revises using the critique as feedback
- [ ] Parallelize Search and Scrape stages using LangGraph's parallel node execution
- [ ] Add a Supervisor agent that dynamically assigns tasks to sub-agents based on topic complexity
- [ ] Export final report to a formatted PDF

---

## License

MIT License. Built as a learning project  use it, break it, improve it.

---

> Built by Qasim Mehr  github.com/qasim-mehar · linkedin.com/in/qasim-mehr