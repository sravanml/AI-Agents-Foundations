# Chapter 2 Examples: Detailed Explanation & Q&A

A comprehensive guide to understanding all 4 agent examples and their differences.

---

## Quick Overview: The 4 Examples

| # | Example | What It Does | Why Build It | Use Case |
|---|---------|-------------|-------------|----------|
| 1 | **Mock Agent** | Fake search tool | Learn how agents work | Learning & testing |
| 2 | **Tavily Custom** | Real search (raw SDK) | Understand the details | Educational |
| 3 | **LangChain Tool** | Real search (built-in) | Production approach | Real applications |
| 4 | **Structured Output** | Structured JSON response | Production quality | APIs & services |

---

## Example 1: Mock Agent

### What Is It Trying to Achieve?

**Goal:** Demonstrate how agents work WITHOUT needing real API calls.

Think of it like a **flight simulator**:
- You learn to fly in a simulator first
- No real airplane needed
- You understand the concepts
- Then you fly a real plane

### The Code

```python
@tool
def search(query: str) -> str:
    """Search the internet for information."""
    # This is FAKE - always returns the same thing
    return f"Mock results for '{query}': This is a simulated search result."
```

### What Happens When You Run It

```
User: "What's the weather in Tokyo?"
         ↓
Agent: "I should use the search tool"
         ↓
Search Tool Called: search("weather in Tokyo")
         ↓
Tool Returns: "Mock results for 'weather in Tokyo': ..."
         ↓
Agent: "The tool returned fake data, so I can't trust it"
       "I should tell the user I need real data"
         ↓
Final Answer: "I can't provide real-time weather..."
```

### Why Use This?

✅ **No API keys needed** — Test without credentials  
✅ **Fast** — No network calls  
✅ **Safe** — Can't accidentally cost money  
✅ **Learning** — Understand the flow first  

### Key Question: Why Didn't The Agent Use The Tool?

**Q: The agent saw the search tool but didn't use it. Why?**

A: The LLM is smart! It recognized:
- The tool returns fake data
- The question needs real data
- Using fake data would give wrong answers
- So it decided not to use the tool

This shows **agent reasoning** — it makes intelligent decisions about whether to use tools.

---

## Example 2: Tavily Custom Agent

### What Is It Trying to Achieve?

**Goal:** Show how to integrate a REAL API (Tavily) directly using the raw SDK.

This is like **learning to drive a manual transmission**:
- You understand every gear shift
- You control everything manually
- You see exactly what's happening

### The Code

```python
@tool
def search(query: str) -> str:
    """Search the internet for current information using Tavily."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query=query, max_results=3)
    
    # Format the results nicely for the LLM
    formatted = "\n".join([
        f"- {r['title']}: {r['content']}"
        for r in results['results']
    ])
    
    return formatted
```

### Step by Step: What's Happening

```
User: "Tell me one recent news in technology"
         ↓
Agent: "I should search for this"
         ↓
Tool Called: search("recent news in technology")
         ↓
Inside search():
   1. Create Tavily client
   2. Call real Tavily API
   3. Get back actual search results
   4. Format them nicely (title + content)
   5. Return formatted string
         ↓
Tool Returns: "Search Results:
              1. Intel and Broadcom warn about AI capital crunch
                 Intel and Broadcom CEOs warn that..."
         ↓
Agent: Reads real search results
       Thinks: "Great! I have real information now"
         ↓
Final Answer: "Intel and Broadcom CEOs warn that a capital 
              crunch could become AI's biggest bottleneck..."
```

### Why Use This?

✅ **See all the details** — You control formatting, API calls, everything  
✅ **Learn the mechanics** — Understand how Tavily works  
✅ **Custom formatting** — Adapt results however you want  
❌ **More code** — Lots of manual work  
❌ **More bugs** — You have to handle errors  

### Key Questions

**Q: Why do we format the results?**

A: The LLM needs clean, readable text. Raw API responses have too much data. We extract:
- Title (what is this result?)
- Content (what does it say?)
We skip the raw JSON, URLs, metadata, etc.

**Q: What's `max_results=3`?**

A: Limit to 3 results. Why?
- Too many results = confusing for LLM
- More results = higher cost
- 3 is usually enough to answer questions
- Trade-off between quality and cost

**Q: Why use `TavilyClient` directly?**

A: To understand what's happening:
1. Create client
2. Call API
3. Get response
4. Format it

This teaches you the full flow. In production, you'd use LangChain's wrapper (Example 3).

---

## Example 3: LangChain TavilySearch Tool

### What Is It Trying to Achieve?

**Goal:** Use a PRODUCTION-READY tool that LangChain provides.

This is the **standard, recommended approach** for production code.

### The Code

```python
from langchain_tavily import TavilySearch

search_tool = TavilySearch(max_results=3)
tools = [search_tool]

agent = create_agent(model=llm, tools=tools)
```

### What's Different?

| Aspect | Example 2 (Custom) | Example 3 (LangChain) |
|--------|------------------|----------------------|
| **Code** | 15+ lines | 3 lines |
| **Error Handling** | You write it | Pre-built |
| **Formatting** | You write it | Pre-optimized |
| **Testing** | You test it | Already tested |
| **Maintenance** | You maintain it | LangChain maintains |
| **Performance** | Custom optimized | Pre-optimized for agents |

### Step by Step

```
User: "What's the current Bitcoin price?"
         ↓
Agent: Sees the TavilySearch tool
       "I'll use this to search"
         ↓
TavilySearch executes internally:
   - Calls Tavily API
   - Formats results automatically
   - Handles errors gracefully
   - Returns clean data optimized for LLM
         ↓
Agent: Reads the results
       "Bitcoin is $82,471"
         ↓
Final Answer: "Bitcoin is approximately $82,471 USD
              (0.68% increase in 24 hours)"
```

### Why Use This in Production?

✅ **Less code** — 3 lines instead of 15  
✅ **Fewer bugs** — Tested and maintained  
✅ **Better error handling** — Handles API failures gracefully  
✅ **Optimized for agents** — Results formatted specifically for LLMs  
✅ **Consistency** — Works reliably across projects  

### Key Question

**Q: Why is Example 3 better than Example 2?**

A: Direct comparison:

**Example 2 Problems:**
- You write 15 lines of code (more to maintain)
- You handle error cases (what if API fails? Network timeout?)
- You format results (what if Tavily changes response format?)
- You test it (need to test formatting, error cases)
- You maintain it (if Tavily updates, you update your code)

**Example 3 Advantages:**
- LangChain writes the 15 lines (tested by many users)
- Error handling built-in (retry logic, timeouts handled)
- Results pre-formatted for LLMs (optimized)
- Already tested with thousands of agents
- Updated by LangChain team (you get improvements automatically)

**Real-world impact:**
- Example 2 works today, might break if Tavily changes
- Example 3 keeps working because LangChain maintains it
- Example 2: You spend 2 hours testing and debugging
- Example 3: Works immediately, spend time on actual features

This is about **letting experts handle the integration** so you focus on your application.

---

## Example 4: Structured Output with Pydantic

### What Is It Trying to Achieve?

**Goal:** Make the agent return data in a STRUCTURED FORMAT (JSON) instead of plain text.

This is crucial for production because:
- Websites need JSON, not text
- Apps need to parse the data
- You need guarantees about what fields exist

### The Code

```python
class WeatherInfo(BaseModel):
    location: str = Field(description="The location for weather")
    temperature: str = Field(description="Current temperature")
    condition: str = Field(description="Weather condition")
    source: str = Field(description="Where the info came from")

class WeatherResponse(BaseModel):
    weather: WeatherInfo
    confidence: float

agent = create_agent(
    model=llm,
    tools=tools,
    response_format=WeatherResponse  # ← This is the key
)
```

### What Changed?

**Without Structured Output (Examples 1-3):**
```
Agent Response: "It's currently 16°C and sunny in Paris with no precipitation..."
# This is just a string. How do I parse it?
# How do I know if it has temperature? Maybe the model forgot?
# What if I need to use this in an API?
```

**With Structured Output (Example 4):**
```
Agent Response:
{
  "weather": {
    "location": "Paris",
    "temperature": "16°C",
    "condition": "Sunny",
    "source": "Tavily search"
  },
  "confidence": 0.95
}

# Perfect! I know exactly:
# - location is here
# - temperature is here
# - confidence is here
# Can parse it automatically!
```

### Why Is This Important?

**Scenario 1: Building an API**
```
Frontend: "Give me weather for Paris"
         ↓
Your API calls the agent
         ↓
Agent returns: {"location": "Paris", "temperature": "16°C", ...}
         ↓
Frontend: Receives clean JSON, displays it perfectly
```

**Scenario 2: Building an App**
```
Your app calls the agent
         ↓
Agent returns: WeatherResponse object
         ↓
Your code: response.weather.temperature  # Easy!
```

### How Does Pydantic Help?

```python
class WeatherResponse(BaseModel):
    weather: WeatherInfo = Field(...)
    confidence: float = Field(...)
```

Pydantic does:
1. ✅ **Defines structure** — What fields must exist?
2. ✅ **Validates data** — Is temperature a number?
3. ✅ **Type safety** — I know temperature is a string
4. ✅ **Documentation** — The description explains each field
5. ✅ **Serialization** — Easily convert to JSON

### Key Question

**Q: When should I use structured output?**

A:
- ✅ **YES** — Building APIs, web apps, mobile apps
- ✅ **YES** — Data needs to be parsed programmatically
- ✅ **YES** — You need guarantees about fields
- ❌ **NO** — Just experimenting/learning
- ❌ **NO** — Just chatting with a user

---

## Side-by-Side Comparison

### Code Complexity

```
Example 1: 10 lines    (simple, fake)
Example 2: 25 lines    (complex, real API)
Example 3: 3 lines     (simple, real API)
Example 4: 20 lines    (complex structure)
```

### What They Return

```
Example 1: String
           "I can't provide real-time weather..."

Example 2: String
           "Search Results:\n1. Intel warns..."

Example 3: String
           "Bitcoin is approximately $82,471..."

Example 4: JSON Object
           {
             "weather": {...},
             "confidence": 0.95
           }
```

### When to Use Each

```
Example 1: Learning & testing
Example 2: Understanding how APIs work
Example 3: Production (real app)
Example 4: Production (API endpoint)
```

---

## Understanding Agent Flow

### The Basic Loop

```
┌─────────────────────────┐
│   Agent Starts          │
│   Input: "Question?"    │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│   LLM Thinks            │
│   "Do I need a tool?"   │
└────────┬────────────────┘
         ↓
    ┌────────────┐
    │ Yes → Use Tool   No → Answer directly
    │
    ↓
┌─────────────────────────┐
│   Tool Executes         │
│   (Search, API call)    │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│   LLM Reads Result      │
│   "Now I have data"     │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│   LLM Generates Answer  │
│   Returns result        │
└─────────────────────────┘
```

---

## Common Questions & Answers

### Q: Why does Example 1 not use the tool?

**A:** The agent is smart. It knows:
- The tool is fake (returns mock data)
- Real data is needed for weather
- Using fake data → wrong answer
- Best choice: admit it can't help

This is **intelligent reasoning**.

### Q: Can I use Example 2 in production?

**A:** Technically yes, but:
- ✅ It works
- ❌ Harder to maintain (15 lines of code)
- ❌ Error handling is manual
- ❌ Other developers might not understand it

**Better:** Use Example 3 (LangChain's tool)

### Q: When do I need Pydantic (Example 4)?

**A:** When you need the output to be:
- Serializable to JSON
- Parseable by other code
- Guaranteed to have certain fields
- Used in APIs or services

If you're just chatting with a user? Example 3 is fine.

### Q: What's the difference between Examples 2 and 3?

**A:** Same result, different approach:

**Example 2 (DIY):**
```python
# You do everything
client = TavilyClient(...)
results = client.search(...)
formatted = format_results(results)
return formatted
```

**Example 3 (LangChain):**
```python
# LangChain does it for you
tool = TavilySearch(...)
# Done! It handles search, formatting, errors
```

Example 3 is better because you get a tested, maintained solution.

### Q: Why is Example 4 output broken?

Look at the output:
```
Raw: {"weather":{"location":"Paris","temperature":"Unavailable",...},"confidence":0.2}
Parsed as Pydantic model:
```

It says "Unavailable" because weather is hard to get from web search. The agent tried but couldn't find current weather in Paris. The `confidence: 0.2` means it's only 20% confident.

This is actually **correct behavior** — the agent is honest about what it doesn't know!

---

## Learning Path

**Step 1:** Run Example 1
- Understand how agents work
- See the basic flow

**Step 2:** Run Example 2
- Learn how to integrate real APIs
- See the details of what happens

**Step 3:** Run Example 3
- Compare with Example 2
- See how LangChain simplifies things
- This is production approach

**Step 4:** Understand Example 4
- Learn when you need structured data
- See how Pydantic helps

**Step 5:** Build your own
- Create a custom tool
- Use real API
- Return structured data

---

## Key Takeaways

1. **Example 1 = Learning Tool**
   - Simplest, no APIs, teaches concepts

2. **Example 2 = Educational**
   - Show how APIs actually work
   - See all the details

3. **Example 3 = Production Standard**
   - Use this in real apps
   - Clean, simple, reliable

4. **Example 4 = Production Plus**
   - Use this for APIs and services
   - Guaranteed structure

---

## Next Steps

After studying these examples, you can:
- [ ] Run each example and understand the output
- [ ] Modify Example 1 to add a different fake tool
- [ ] Try Example 3 with different questions
- [ ] Build your own agent with a custom tool

