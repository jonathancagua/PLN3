
from typing import AsyncGenerator, Literal
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import  create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.store.memory import InMemoryStore
from langmem.short_term import SummarizationNode

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langgraph_supervisor import create_supervisor

from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun

from .prompt import *
from src.tools import tools  
from .state import State


arxiv = ArxivAPIWrapper(
    top_k_results = 3,
    ARXIV_MAX_QUERY_LENGTH = 300,
    load_max_docs = 3,
    load_all_available_meta = False,
    doc_content_chars_max = 10000
)

arxiv_tool = ArxivQueryRun(api_wrapper=arxiv)
tools.append(arxiv_tool)

checkpointer = InMemorySaver()  # For thread-level state persistence
memory_store = InMemoryStore() 

# Base class to provide shared LLM
class LLMProvider:
    def __init__(
        self,
        model: str = "llama3.2:latest",
        temperature: float = 0.1,
        provider: Literal["auto","ollama","groq"] = "auto",   # "auto", "ollama", "groq"
    ):
        groq_api_key = os.getenv("GROQ_API_KEY")

        # Ollama LLM
        ollama_llm = ChatOllama(
            model=model,
            temperature=temperature,
        )

        # Groq LLM (only init if API key available)
        groq_llm = None
        if groq_api_key:
            groq_llm = ChatGroq(
                model="openai/gpt-oss-120b",
                temperature=0,
                max_tokens=None,
                reasoning_format="parsed",
                timeout=None,
                api_key=groq_api_key,
                max_retries=2,
            )

        # Selection logic
        if provider == "ollama":
            self.llm = ollama_llm
        elif provider == "groq":
            if not groq_llm:
                raise ValueError("GROQ_API_KEY not found, cannot use Groq provider.")
            self.llm = groq_llm
        elif provider == "auto":
            # Prefer Groq if available, else Ollama
            self.llm = groq_llm if groq_llm else ollama_llm
        else:
            raise ValueError(f"Unknown provider '{provider}'. Choose 'auto', 'ollama', or 'groq'.")


class SummarizerAgent(LLMProvider):
    def __init__(self, model: str = "llama3.2:latest", temperature: float = 0.1):
        super().__init__(model=model, temperature=temperature,provider="ollama")

        self.agent = create_react_agent(
            model=self.llm,
            prompt=summarizer_prompt,
            tools=[],   # no external tools
            name="SummarizerAgent",
            state_schema=State,
        )


class ResearchAssistant(LLMProvider):
    def __init__(self, model: str = "llama3.2:latest", temperature: float = 0.1):
        super().__init__(model=model, temperature=temperature,provider="groq")

        self.agent = create_react_agent(
            model = self.llm,
            prompt=system_prompt,
            tools = tools,
            name="ResearchAssistant",
            state_schema=State,
        )


summarization_node = SummarizationNode( 
    token_counter=count_tokens_approximately,
    model=  ChatOllama(model="llama3.2:latest", temperature=0.1),
    max_tokens=768,
    max_summary_tokens=512,
    output_messages_key="llm_input_messages",
    )

supervisor = create_supervisor(
    agents=[ ResearchAssistant().agent, SummarizerAgent().agent],
    model=ChatOllama(model="llama3.2:latest", temperature=0.1),
    prompt=supervisor_prompt,
    pre_model_hook= summarization_node,
).compile(checkpointer=checkpointer, store=memory_store)


async def query( q: str, session_id:str) -> AsyncGenerator[str, None]:
    state = {"messages": [HumanMessage(content=q)]}
    config = {"configurable": {"thread_id": session_id}}
    async for  event in supervisor.astream_events(
        state,
        version="v2",
        config=config,
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"].get("chunk")
            if chunk and hasattr(chunk, "content"):
                text = chunk.content
                if text:
                    # Yield raw token text
                    yield text

async def interactive( session_id: str = None):
    print("Research Assistant (LangGraph + ChatOllama + Groq). Type 'exit' to quit.")
    while True:
        try:
            q = input("\nQuery> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye"); break
        if q.lower() in ("exit", "quit"):
            break
        async for response in query(q, session_id):
            print(response, end="", flush=True)
