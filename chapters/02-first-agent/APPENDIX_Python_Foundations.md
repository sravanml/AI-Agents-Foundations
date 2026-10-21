# Appendix: Python Foundations for Agents

**Quick reference for Python concepts used in Chapter 2.**

Understanding these concepts is essential for building agents.

---

## Table of Contents

1. [Functions and Parameters](#functions-and-parameters)
2. [Type Hints](#type-hints)
3. [Docstrings](#docstrings)
4. [Args and Returns](#args-and-returns)
5. [Decorators](#decorators)
6. [Pydantic Models](#pydantic-models)

---

## Functions and Parameters

### What is a Function?

A function is a block of code that does something and can be reused.

```python
def greet(name):
    return f"Hello, {name}!"

# Use the function
result = greet("Alice")
print(result)  # Hello, Alice!
```

### What is a Parameter?

A **parameter** is the input a function receives.

In the example above, `name` is a parameter.

```python
def greet(name):  # ← name is the parameter
    return f"Hello, {name}!"

greet("Alice")  # ← "Alice" is passed to the parameter
```

### Real Agent Example

```python
@tool
def search(query: str) -> str:
    """Search the internet."""
    return f"Results for: {query}"
```

**Here:**
- `query` is the parameter
- It expects a string (text)
- When the agent calls it: `search(query="weather in Tokyo")`
- `query` receives: `"weather in Tokyo"`

---

## Type Hints

Type hints tell Python (and the LLM!) what types of data parameters should be.

### Basic Types

```python
name: str = "Alice"           # String (text)
age: int = 30                 # Integer (whole number)
height: float = 5.8           # Float (decimal number)
is_student: bool = True       # Boolean (True/False)
```

### Function Type Hints

```python
def add(a: int, b: int) -> int:
    return a + b
    
# Breakdown:
# a: int        ← parameter 'a' must be an integer
# b: int        ← parameter 'b' must be an integer
# -> int        ← function returns an integer
```

### List Type Hints

```python
from typing import List

def process_items(items: List[str]) -> int:
    # input: a list of strings
    # output: an integer
    return len(items)

process_items(["apple", "banana"])  # 2
```

### Why Type Hints Matter for Agents

The LLM **needs type hints** to know:
- What arguments to pass to a tool
- What type of data the tool returns
- How to handle the result

```python
# Good - LLM knows what to do
def search(query: str) -> str:
    """Search the internet."""
    pass

# Bad - LLM is confused
def search(q):  # No type hints!
    pass
```

Without type hints, the LLM doesn't know if `query` should be a string, number, or list.

---

## Docstrings

### What is a Docstring?

A **docstring** is a string that explains what a function does.

It's like an **instruction manual** written inside the function.

### Where It Goes

```python
def greet(name: str) -> str:
    """Say hello to someone."""  # ← This is the docstring
    return f"Hello, {name}!"
```

The docstring comes right after the function definition.

### Single-line Docstring

```python
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

Use for simple functions.

### Multi-line Docstring

```python
def weather(city: str, unit: str = "celsius") -> str:
    """Get weather information for a city.
    
    This function retrieves current weather
    for the specified city.
    
    Args:
        city: The city name (e.g., "Tokyo", "Paris")
        unit: Temperature unit ("celsius" or "fahrenheit")
    
    Returns:
        A string with weather information
    
    Example:
        >>> weather("Tokyo")
        "Weather in Tokyo: 20°C"
    """
    return f"Weather in {city}: 20°"
```

Use for complex functions.

### Why Docstrings Matter

**For Humans:** Easy to understand what the function does

```python
help(weather)
# Displays the docstring so you know how to use it
```

**For the LLM:** The LLM READS docstrings to understand tools!

```python
@tool
def search(query: str) -> str:
    """Search the internet for information.
    
    Args:
        query: The search query (what to search for)
    
    Returns:
        Search results as a string
    """
    pass
```

When you give this tool to an agent, the LLM reads:
- Function name: `search`
- Purpose: "Search the internet for information"
- Parameter: `query` (a string) = "what to search for"
- Returns: a string

The LLM uses this to decide:
- "Should I use this tool?" → YES (user asked a search question)
- "What to pass?" → Extract the search term from the user's question

---

## Args and Returns

### What is Args?

**Args** = Arguments = Parameters = Inputs

It's a list of what information the function needs.

```python
def weather(city: str, unit: str = "celsius") -> str:
    """Get weather.
    
    Args:
        city: The city name (e.g., "Tokyo", "Paris")
        unit: Temperature unit ("celsius" or "fahrenheit")
    """
    return f"Weather in {city}: 20°{unit[0].upper()}"
```

**The Args section tells:**
- `city`: Required parameter, what it means
- `unit`: Optional parameter with default value

### What is Returns?

**Returns** = Output = What the function gives back

```python
def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b
```

**The Returns section tells:**
- The function returns an integer (the sum)

### How LLM Uses Args and Returns

When the agent sees a tool:

```python
@tool
def search(query: str, max_results: int = 5) -> str:
    """Search the internet.
    
    Args:
        query: What you're searching for
        max_results: How many results (default 5)
    
    Returns:
        A string containing search results
    """
    pass
```

**LLM learns:**
- INPUTS (Args):
  - `query` (string): what to search for
  - `max_results` (int, optional): how many results
- OUTPUT (Returns):
  - string: the results

When user asks: "Find me 10 results about Python"

**LLM extracts:**
- query = "Python"
- max_results = 10

**LLM calls:**
```python
search(query="Python", max_results=10)
```

**LLM receives:**
- A string with results

**LLM answers:**
- "Here are 10 results about Python..."

### Complete Args + Returns Example

```python
def calculate_total(price: float, tax_rate: float) -> float:
    """Calculate total price including tax.
    
    Args:
        price: The item price in dollars
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
    
    Returns:
        Total price including tax
    """
    return price * (1 + tax_rate)
```

**Args tell:** What the function needs (price and tax rate)
**Returns tell:** What it gives back (total price)

---

## Decorators

### What is a Decorator?

A **decorator** modifies or enhances a function without changing its code.

It's like adding a wrapper around the function.

```python
@tool  # This is a decorator
def search(query: str) -> str:
    """Search the internet."""
    return f"Results for: {query}"
```

### How It Works

Before the decorator, the function is just a Python function:
```python
def search(query: str) -> str:
    return f"Results for: {query}"
```

After the decorator `@tool`, it's transformed into a LangChain tool:
```python
@tool
def search(query: str) -> str:
    return f"Results for: {query}"

# Now LangChain can:
# - Extract the docstring
# - Get the type hints
# - Call the function when the agent decides to use it
```

### Why Decorators Matter for Agents

The `@tool` decorator tells LangChain:
- "This function is a tool agents can use"
- Extract the docstring (so LLM knows what it does)
- Extract the parameters (so LLM knows what to pass)
- Make it callable from the agent loop

Without `@tool`, it's just a regular function the agent can't use.

---

## Pydantic Models

### What is Pydantic?

Pydantic ensures data is **valid** and **structured**.

It's like a blueprint that says "this data must have these fields with these types."

### Basic Model

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

# Create an instance
person = Person(name="Alice", age=30, email="alice@example.com")

# Access fields
print(person.name)    # Alice
print(person.age)     # 30
```

### With Descriptions (For Agents)

```python
from pydantic import BaseModel, Field

class WeatherInfo(BaseModel):
    location: str = Field(description="The city or region")
    temperature: float = Field(description="Temperature in celsius")
    condition: str = Field(description="Weather condition")

weather = WeatherInfo(
    location="Tokyo",
    temperature=20.5,
    condition="Sunny"
)

print(weather.location)      # Tokyo
print(weather.temperature)   # 20.5
```

### Lists of Objects

```python
from typing import List

class JobPosting(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    salary: int = Field(description="Salary in USD")

class JobResponse(BaseModel):
    jobs: List[JobPosting]
    total_found: int

response = JobResponse(
    jobs=[
        JobPosting(title="Engineer", company="TechCorp", salary=120000),
        JobPosting(title="Designer", company="DesignCo", salary=100000),
    ],
    total_found=2
)

# Access nested data
print(response.jobs[0].title)   # Engineer
print(response.total_found)     # 2
```

### Why Pydantic for Agents

**Without Pydantic:**
```python
# Agent returns: "Found 2 jobs..."
# How do I extract the number? Parse the string?
# What if format changes?
response = "Found 2 jobs: Engineer at TechCorp, Designer at DesignCo"
```

**With Pydantic:**
```python
# Agent returns: structured object
response = JobResponse(
    jobs=[...],
    total_found=2
)

# Easy to use!
print(response.total_found)  # 2
print(response.jobs[0].title)  # Engineer
# Can serialize to JSON automatically
```

**Benefits:**
- ✅ Guaranteed structure
- ✅ Easy to access fields
- ✅ Type-safe
- ✅ Serializes to JSON
- ✅ Perfect for APIs

---

## How It All Works Together for Agents

### Complete Tool Example

```python
from pydantic import BaseModel, Field
from langchain.tools import tool

# Step 1: Define what the tool returns (Pydantic)
class SearchResult(BaseModel):
    title: str = Field(description="Result title")
    url: str = Field(description="Result URL")
    summary: str = Field(description="Result summary")

# Step 2: Define the tool (with docstring + type hints)
@tool
def search(query: str, max_results: int = 5) -> List[SearchResult]:
    """Search the internet for information.
    
    Args:
        query: What to search for (the parameter)
        max_results: Maximum results to return
    
    Returns:
        List of search results with title, URL, and summary
    """
    # Implementation here
    pass
```

**What happens:**
1. `@tool` decorator → Tells LangChain this is a tool
2. `def search(query: str, max_results: int = 5)` → Type hints tell LLM what to pass
3. Docstring (Args/Returns) → LLM understands purpose and parameters
4. `List[SearchResult]` → Returns structured data, not just text
5. `Pydantic BaseModel` → Guaranteed structure

**When agent uses it:**
1. LLM reads: "search tool, needs query and max_results"
2. LLM extracts: query="Python", max_results=10
3. LLM calls: search(query="Python", max_results=10)
4. Tool returns: List of SearchResult objects
5. LLM reads structured data easily
6. LLM provides structured answer

---

## Quick Reference

### Common Patterns in Chapter 2

**Pattern 1: Simple Tool**
```python
@tool
def my_tool(input_param: str) -> str:
    """What this tool does."""
    return f"Result: {input_param}"
```

**Pattern 2: Tool with Multiple Parameters**
```python
@tool
def search(query: str, max_results: int = 5) -> str:
    """Search for information.
    
    Args:
        query: The search term
        max_results: Maximum results to return
    
    Returns:
        Search results as string
    """
    pass
```

**Pattern 3: Tool with Structured Output**
```python
class Result(BaseModel):
    answer: str
    confidence: float

@tool
def answer_question(question: str) -> Result:
    """Answer a question.
    
    Args:
        question: The question to answer
    
    Returns:
        Result with answer and confidence
    """
    pass
```

---

## Summary

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Parameter** | Input to a function | LLM knows what to pass |
| **Type Hint** | `str`, `int`, `float` | LLM knows data types |
| **Docstring** | Function documentation | LLM understands purpose |
| **Args** | List of parameters | LLM knows what to extract |
| **Returns** | What function gives back | LLM knows what to expect |
| **Decorator** | `@tool` wrapper | Makes function a tool |
| **Pydantic** | Data structure | Structured output |

**For Agents:**
- Type hints → Tell LLM what to pass
- Docstrings → Explain what tool does
- Args → Show what to extract from questions
- Returns → Show what format to return
- Pydantic → Structure the output

---

## Next Steps

- Understand each concept with `simple_agent_explained.py`
- Read `EXAMPLES_EXPLAINED.md` for detailed walkthroughs
- Build your own tools with these patterns
