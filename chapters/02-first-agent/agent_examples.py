"""
Chapter 2: Agent Examples
Run each example to see agents in action.
"""

import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

# ============================================================================
# EXAMPLE 1: Mock Agent (Simple - No Real API Calls)
# ============================================================================

def example_1_mock_agent():
    """Your first agent with a fake search tool."""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Mock Agent (Simple Tool)")
    print("="*70)
    
    @tool
    def search(query: str) -> str:
        """Search the internet for information.
        
        Args:
            query: The search query
            
        Returns:
            Search results as a string
        """
        # Fake search - returns mock data
        return f"Mock results for '{query}': This is a simulated search result."
    
    # Create the agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [search]
    agent = create_agent(model=llm, tools=tools)
    
    # Run the agent
    print("\nAgent: I have access to a search tool")
    print("User: What's the weather in Tokyo?")
    print()
    
    response = agent.invoke({
        "messages": [HumanMessage("What's the weather in Tokyo?")]
    })
    
    print("Agent Response:")
    print(response["messages"][-1].content)


# ============================================================================
# EXAMPLE 2: Real Search with Tavily Client (Raw SDK)
# ============================================================================

def example_2_tavily_custom_agent():
    """Agent with real search using Tavily SDK directly."""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Real Search with Tavily Client")
    print("="*70)
    
    try:
        from tavily import TavilyClient
    except ImportError:
        print("Install tavily-python: pip install tavily-python")
        return
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        print("ERROR: TAVILY_API_KEY not found in .env")
        return
    
    @tool
    def search(query: str) -> str:
        """Search the internet for current information using Tavily.
        
        Args:
            query: The search query
            
        Returns:
            Formatted search results
        """
        try:
            client = TavilyClient(api_key=tavily_api_key)
            results = client.search(query=query, max_results=3)
            
            # Format results nicely
            formatted = "Search Results:\n"
            for i, result in enumerate(results.get('results', []), 1):
                formatted += f"\n{i}. {result.get('title', 'No title')}\n"
                formatted += f"   {result.get('content', 'No content')[:200]}...\n"
            
            return formatted
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    # Create the agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [search]
    agent = create_agent(model=llm, tools=tools)
    
    # Run the agent
    print("\nAgent: I have access to REAL web search (Tavily)")
    print("User: What's happening in technology today?")
    print()
    
    response = agent.invoke({
        "messages": [HumanMessage("Tell me one recent news in technology.")]
    })
    
    print("Agent Response:")
    print(response["messages"][-1].content)


# ============================================================================
# EXAMPLE 3: Built-in LangChain Tool (Production Way)
# ============================================================================

def example_3_langchain_tavily_agent():
    """Agent using LangChain's built-in TavilySearch tool."""
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Built-in TavilySearch Tool (Recommended)")
    print("="*70)
    
    try:
        from langchain_tavily import TavilySearch
    except ImportError:
        print("Install langchain-tavily: pip install langchain-tavily")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        print("ERROR: TAVILY_API_KEY not found in .env")
        return
    
    # Create the tool (pre-configured)
    search_tool = TavilySearch(max_results=3)
    tools = [search_tool]
    
    # Create the agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_agent(model=llm, tools=tools)
    
    # Run the agent
    print("\nAgent: Using LangChain's built-in TavilySearch tool")
    print("User: What's the current Bitcoin price?")
    print()
    
    response = agent.invoke({
        "messages": [HumanMessage("What's the current Bitcoin price?")]
    })
    
    print("Agent Response:")
    print(response["messages"][-1].content)


# ============================================================================
# EXAMPLE 4: Structured Output with Pydantic (Production Pattern)
# ============================================================================

def example_4_structured_agent():
    """Agent that returns structured JSON output."""
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Structured Output with Pydantic")
    print("="*70)
    
    try:
        from langchain_tavily import TavilySearch
    except ImportError:
        print("Install langchain-tavily: pip install langchain-tavily")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        print("ERROR: TAVILY_API_KEY not found in .env")
        return
    
    # Define structured output format
    class WeatherInfo(BaseModel):
        location: str = Field(description="The location for weather")
        temperature: str = Field(description="Current temperature")
        condition: str = Field(description="Weather condition")
        source: str = Field(description="Where the info came from")
    
    class WeatherResponse(BaseModel):
        weather: WeatherInfo = Field(description="Weather information")
        confidence: float = Field(description="Confidence level 0-1")
    
    # Create tools
    search_tool = TavilySearch(max_results=2)
    tools = [search_tool]
    
    # Create agent with structured output
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_agent(
        model=llm,
        tools=tools,
        response_format=WeatherResponse
    )
    
    # Run the agent
    print("\nAgent: Returns structured JSON output")
    print("User: What's the weather in Paris?")
    print()
    
    response = agent.invoke({
        "messages": [HumanMessage("What's the weather in Paris?")]
    })
    
    print("Agent Response (Structured):")
    try:
        # Extract structured output
        content = response["messages"][-1].content
        print(f"Raw: {content}")
        print(f"\nParsed as Pydantic model:")
        if isinstance(content, dict):
            weather = WeatherResponse(**content)
            print(f"  Location: {weather.weather.location}")
            print(f"  Temperature: {weather.weather.temperature}")
            print(f"  Condition: {weather.weather.condition}")
            print(f"  Confidence: {weather.confidence}")
    except Exception as e:
        print(f"Note: Structured output requires specific model config: {e}")
        print(f"Raw response: {content}")


# ============================================================================
# Main: Run Examples
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CHAPTER 2: AGENT EXAMPLES")
    print("="*70)
    
    # Run all examples
    example_1_mock_agent()
    
    # Uncomment to run examples that need API keys:
    example_2_tavily_custom_agent()
    example_3_langchain_tavily_agent()
    example_4_structured_agent()
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETE")
    print("="*70)
    print("\nTo run other examples, uncomment them in the main() section")

