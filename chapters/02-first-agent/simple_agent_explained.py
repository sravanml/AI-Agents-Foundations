"""
Chapter 2: Agent Concepts Explained with Code
Based on LangChain book Chapter 2 screenshots
"""

import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

load_dotenv()

print("\n" + "="*80)
print("CHAPTER 2: AGENT CONCEPTS EXPLAINED")
print("="*80)

# ============================================================================
# CONCEPT 1: What is a Tool?
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 1: TOOLS - Functions the Agent Can Call")
print("─"*80)

print("""
A TOOL is a function that an agent can use.

Think of it like giving the LLM access to a real-world tool:
- Like giving a person a calculator
- Or giving them internet access
- Or giving them a phone

The LLM can decide to USE the tool or NOT use it.
""")

# Define a tool using @tool decorator
@tool
def search(query: str) -> str:
    """
    Search the internet for information.
    
    This docstring is IMPORTANT - the LLM reads this to understand
    what the tool does and what arguments to pass.
    
    Args:
        query: The search query (what to search for)
    
    Returns:
        Search results as a string
    """
    # For now, return fake data
    return f"Search results for '{query}': Found some information..."

print("Tool created: 'search'")
print("What the LLM sees:")
print(f"  - Name: search")
print(f"  - Docstring: 'Search the internet for information'")
print(f"  - Arguments: query (type: str)")
print(f"  - Returns: str")

# ============================================================================
# CONCEPT 2: Creating an Agent
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 2: CREATING AN AGENT")
print("─"*80)

print("""
An AGENT is:
  - An LLM (the brain)
  - Plus tools (the hands)
  - Plus a loop that decides when to use tools

When you create an agent, you give it:
  1. An LLM (ChatOpenAI, Claude, etc.)
  2. A list of tools it can use
  3. It learns to use them intelligently
""")

# Create the LLM (the brain)
llm = ChatOpenAI(model="gpt-4o", temperature=0)
print("✓ Created LLM: ChatOpenAI(gpt-4o)")

# Create the agent with tools
tools = [search]  # List of tools the agent can use
agent = create_agent(model=llm, tools=tools)
print("✓ Created agent with tools: [search]")

# ============================================================================
# CONCEPT 3: How Agents Think (The ReAct Loop)
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 3: THE ReAct PATTERN - How Agents Think")
print("─"*80)

print("""
ReAct = Reasoning + Acting

When you ask an agent a question, it goes through a loop:

┌─────────────────────────────────────────┐
│  STEP 1: REASON                         │
│  Agent thinks: "What do I need to do?"  │
│  "Should I use a tool?"                 │
│  "Which tool should I use?"             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 2: ACT                            │
│  Agent calls a tool                     │
│  Example: search("weather in Tokyo")    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 3: OBSERVE                        │
│  Agent reads the tool's response        │
│  "I got back these search results..."   │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  STEP 4: REASON AGAIN (Loop Back)       │
│  Agent thinks: "Now I have the info"    │
│  "Time to answer the user's question"   │
└─────────────────────────────────────────┘
               ↓
         FINAL ANSWER
""")

# ============================================================================
# CONCEPT 4: Running the Agent (See the ReAct Loop)
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 4: RUNNING THE AGENT - Watch the ReAct Loop")
print("─"*80)

print("\nUser Question: 'What is Python programming?'")
print("\nAgent processes this:\n")

# Run the agent
response = agent.invoke({
    "messages": [HumanMessage("What is Python programming?")]
})

print("Agent's Final Answer:")
print(response["messages"][-1].content)

print("\n" + "─"*80)
print("What Happened Above:")
print("─"*80)
print("""
1. REASON: Agent saw the question
          "This is about Python - I might need to search"

2. ACT: Agent decided whether to use the search tool
       "I actually know about Python already"
       "I don't need external search"

3. OBSERVE: (skipped - no tool was called)

4. REASON: Agent gives direct answer
          "Python is a programming language..."

Notice: The agent was SMART enough to know it didn't need
to search - it has this knowledge already!
""")

# ============================================================================
# CONCEPT 5: Tools with Real Impact
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 5: When Agents WILL Use Tools")
print("─"*80)

print("""
The agent will USE tools when it needs:
- Current information (weather, stock prices)
- Real-time data (news, social media)
- Specific facts (Wikipedia, databases)
- Mathematical calculations

The agent will NOT use tools when:
- It already knows the answer
- The question is philosophical
- No tool can help
""")

@tool
def weather(city: str) -> str:
    """Get current weather for a city."""
    # Fake implementation
    return f"Weather in {city}: Sunny, 20°C"

tools_with_weather = [search, weather]
agent_with_weather = create_agent(model=llm, tools=tools_with_weather)

print("\nNew agent created with tools: [search, weather]")
print("\nUser Question: 'What is the weather in Tokyo?'")
print()

response2 = agent_with_weather.invoke({
    "messages": [HumanMessage("What is the weather in Tokyo?")]
})

print("Agent's Answer:")
print(response2["messages"][-1].content)

print("\n" + "─"*80)
print("What Happened:")
print("─"*80)
print("""
1. REASON: "User asked about weather"
          "I have a weather tool available"
          "I should use it!"

2. ACT: Agent calls weather("Tokyo")
       Gets back: "Weather in Tokyo: Sunny, 20°C"

3. OBSERVE: Agent reads the result

4. REASON: Agent answers based on tool output
          "Tokyo is sunny, 20°C"

The key difference from the previous example:
- PREVIOUS: Agent knew the answer, no tool needed
- THIS: Agent had a tool and used it because it was relevant
""")

# ============================================================================
# CONCEPT 6: Understanding Type Hints
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 6: Why Type Hints Matter")
print("─"*80)

print("""
Look at how we defined the tool:

    @tool
    def search(query: str) -> str:
        ...

The LLM needs to know:
- Input: query is a STRING (not a number, not a list)
- Output: returns a STRING

Without type hints:

    def search(query):  # ← LLM is confused!
        ...

The LLM won't know:
- What type should query be?
- What will the function return?
- This makes it hard to use the tool correctly

TYPE HINTS = Instructions for the LLM
""")

# ============================================================================
# CONCEPT 7: Multiple Tools
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 7: Agent with Multiple Tools")
print("─"*80)

print("""
Agents can have MANY tools.

The agent learns to:
1. Identify which tool is needed
2. Use the right tool for each question
3. Combine information from multiple tools

Example:
- Tool 1: search (web search)
- Tool 2: weather (weather info)
- Tool 3: calculator (math)

If user asks "What's 2+2 and the weather?" →
Agent uses BOTH tools automatically
""")

# ============================================================================
# CONCEPT 8: Structured Output
# ============================================================================

print("\n" + "─"*80)
print("CONCEPT 8: Structured Output (Production)")
print("─"*80)

print("""
By default, agents return plain text:
  "The weather is sunny and 20°C"

For production apps, you need structured data (JSON):
  {
    "temperature": 20,
    "condition": "sunny",
    "unit": "celsius"
  }

This is where Pydantic comes in.
""")

class WeatherInfo(BaseModel):
    """Structure for weather data"""
    temperature: int = Field(description="Temperature in celsius")
    condition: str = Field(description="Weather condition")
    humidity: int = Field(description="Humidity percentage")

print("Pydantic Model defined:")
print("  - temperature: int")
print("  - condition: str")
print("  - humidity: int")

print("""
Now the agent knows EXACTLY what format to return.
This is critical for:
- APIs (need JSON)
- Web apps (need structured data)
- Mobile apps (need consistent format)
""")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("SUMMARY: The ReAct Agent Flow")
print("="*80)

print("""
TOOLS:          Functions the agent can call
                Defined with @tool decorator

AGENT:          LLM + Tools + Decision Loop

ReAct LOOP:     Reason → Act → Observe → Reason → Answer

TYPE HINTS:     Tell LLM what inputs/outputs are

TOOLS MATTER:   Only use them when needed
                Agent is smart about when to use tools

STRUCTURED:     For production, return JSON not text

EXAMPLE FLOW:
  User: "What's the weather in Tokyo?"
    ↓
  Agent Thinks: "I need current weather, I'll use the weather tool"
    ↓
  Agent Calls: weather("Tokyo")
    ↓
  Tool Returns: {"temp": 20, "condition": "sunny"}
    ↓
  Agent Thinks: "Got the data, now I'll answer"
    ↓
  Final: "It's sunny and 20°C in Tokyo"
""")

print("\n" + "="*80)
print("CONCEPTS COVERED")
print("="*80)
print("""
✓ What tools are
✓ How to create tools (@tool decorator)
✓ How to create agents
✓ The ReAct pattern (Reason → Act → Observe)
✓ Why type hints matter
✓ When agents use tools (or don't)
✓ Multiple tools in one agent
✓ Structured output with Pydantic
""")

print("\nNext: Read EXAMPLES_EXPLAINED.md for detailed breakdown of all 4 examples\n")

