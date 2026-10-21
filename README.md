# LangChain Learning Module: From Zero to Your First Chain

A step-by-step learning guide to understand LangChain fundamentals through hands-on examples.

---

## Table of Contents

1. [What is LangChain?](#what-is-langchain)
2. [Core Concepts](#core-concepts)
3. [Setup & Installation](#setup--installation)
4. [Your First Chain](#your-first-chain)
5. [Understanding the Code](#understanding-the-code)
6. [Debugging with VS Code](#debugging-with-vs-code)
7. [Tracing with LangSmith](#tracing-with-langsmith)
8. [Key Takeaways](#key-takeaways)

---

## What is LangChain?

LangChain is a framework for developing applications powered by language models (LLMs). It simplifies:
- Building chains of prompts and LLM calls
- Managing data flow between components
- Integrating with external tools and APIs
- Tracing and debugging LLM applications

Think of it as a toolbox that helps you compose LLMs with templates, memory, tools, and more—without reinventing the wheel.

---

## Core Concepts

### 1. **PromptTemplate**

A reusable template for prompts with placeholders for dynamic data.

**Why use templates instead of f-strings?**

```python
# ❌ F-string - values baked in immediately
info = "Elon Musk"
msg = f"Summarize: {info}"  # Hard to reuse, values locked in

# ✅ Template - reusable with different data
template = PromptTemplate(
    input_variables=["info"],
    template="Summarize: {info}"
)
msg1 = template.format(info="Elon Musk")
msg2 = template.format(info="Steve Jobs")  # Same template, different data
```

**Benefits:**
- Consistency across multiple runs
- Easy A/B testing different prompts
- Cleaner code organization
- Better for production applications

### 2. **LLMs (Language Models)**

The brain of the operation. In this guide, we use OpenAI's `ChatOpenAI`.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o")
```

**Parameters:**
- `temperature=0`: Deterministic responses (no randomness)
- `model="gpt-4o"`: Which model to use

### 3. **Chains**

Combining a PromptTemplate and an LLM into a pipeline.

```python
# Pipe operator (|) chains components together
chain = summary_prompt_template | llm

# Execute the chain
response = chain.invoke(input={"information": information})
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- OpenAI API key
- LangSmith account (optional, for tracing)

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
python-dotenv==1.0.0
langchain-core>=0.1.33
langchain-openai>=0.1.0
langsmith>=0.1.0
```

### Step 3: Configure Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_AGENT_ID=your_project_name
LANGSMITH_AGENT_ENVIRONMENT=production
```

**Never commit `.env` to git!** It contains secrets.

---

## Your First Chain

Here's the complete code to build a summarization chain:

```python
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

def main():
    # 1. Your input data
    information = """Elon Reeve Musk is a business magnate and investor. 
    He is the founder, CEO and chief engineer of SpaceX; 
    angel investor, CEO and product architect of Tesla, Inc.; 
    owner and 'Chief Twit' of Twitter; 
    founder of The Boring Company; co-founder of Neuralink and OpenAI; 
    and president of the Musk Foundation."""
    
    # 2. Create a reusable template
    summary_template = """
given the information {information} about a person I want you to create:
1. A short summary
2. two interesting facts about them
"""
    
    # 3. Bind the template with input variables
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template
    )
    
    # 4. Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
    # 5. Create the chain (template | llm)
    chain = summary_prompt_template | llm
    
    # 6. Execute the chain
    response = chain.invoke(input={"information": information})
    
    # 7. Print the result
    print(response.content)

if __name__ == "__main__":
    main()
```

**What happens step-by-step:**

1. **Load environment** → Reads API keys from `.env`
2. **Create template** → A reusable prompt structure with `{information}` placeholder
3. **Bind variables** → Tell LangChain which variables are dynamic
4. **Initialize LLM** → Connect to OpenAI
5. **Pipe components** → `template | llm` creates a chain
6. **Execute** → `invoke()` fills the template and sends to LLM
7. **Get response** → Extract `content` from the response

---

## Understanding the Code

### Indentation in Python

Python uses **indentation to define code blocks**—not curly braces like other languages.

```python
def main():
    x = 1  # Indented = inside the function
    print(x)  # Indented = inside the function
print("Done")  # Not indented = outside the function
```

Missing indentation = `IndentationError`.

### F-strings vs Jinja2 Templates

**F-strings (evaluated immediately):**
```python
name = "Elon"
msg = f"Hello, {name}"  # Value locked in NOW
```

**Jinja2 Templates (evaluated later):**
```python
template = PromptTemplate(
    input_variables=["name"],
    template="Hello, {name}"
)
msg = template.format(name="Elon")  # Value filled in WHEN YOU CALL format()
```

**Why LangChain uses Jinja2:**
- Reusable across multiple inputs
- Easy to test different prompt versions
- Better for scaling applications
- Cost-efficient (same prompt structure = consistent behavior)

---

## Debugging with VS Code

### Setting Breakpoints

1. Open your Python file
2. Click on the **line number** where you want to pause
3. A red dot appears—that's your breakpoint

### Running in Debug Mode

1. Press **F5** to start debugging
2. Code pauses at your breakpoint
3. Check the **Variables panel** on the left to inspect values

**While paused, you can:**
- **Hover over variables** to see their values
- **F10** = Step to next line
- **F11** = Step into a function
- **Debug Console** = Type commands to inspect variables

**Example:** Set a breakpoint before `response = chain.invoke(...)` to see:
- What `information` contains
- What `chain` is composed of
- What `template` looks like

Then press F10 to execute that line and inspect `response`.

---

## Tracing with LangSmith

LangSmith records every step your chain takes—useful for debugging and monitoring.

### Setup

1. Go to **https://smith.langchain.com**
2. Sign up or log in
3. Go to **Settings** → **API Keys** → Create a new key
4. Add to your `.env`:

```
LANGSMITH_API_KEY=your_key
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_AGENT_ID=your_project_name
```

### What You See in LangSmith

After running your chain, go to **LangSmith → Tracing**. You'll see:

- **Input** → The filled prompt sent to the LLM
- **Output** → The LLM's response
- **Metadata** → Tokens used, execution time, cost
- **Nested calls** → If your chain has sub-steps

This is invaluable for:
- Debugging prompt issues
- Monitoring LLM behavior
- Comparing different prompt versions
- Estimating costs

---

## Key Takeaways

### What You Learned

✅ **PromptTemplate** → Reusable templates with placeholders  
✅ **LLMs** → How to initialize and use language models  
✅ **Chains** → Piping components together with `|` operator  
✅ **Templates vs F-strings** → Why Jinja2 templates scale better  
✅ **Environment Variables** → Secure API key management  
✅ **Debugging** → Using VS Code breakpoints to inspect values  
✅ **Tracing** → Monitoring your chain with LangSmith  

### Next Steps

1. **Modify the prompt** → Change what the LLM is asked to do
2. **Add memory** → Store conversation history
3. **Use tools** → Let LLMs call functions
4. **Build agents** → Create chains that decide what to do next
5. **Create custom chains** → Combine multiple LLMs and templates

### Common Mistakes to Avoid

❌ Hardcoding API keys in code → Use `.env` files  
❌ Using f-strings for production → Use PromptTemplate  
❌ Forgetting to activate virtual environment → Always `source venv/bin/activate`  
❌ Not checking environment variables → Use debug.py to verify  
❌ Ignoring LangSmith traces → Traces show what went wrong  

---

## Resources

- **LangChain Docs:** https://python.langchain.com
- **OpenAI API:** https://platform.openai.com
- **LangSmith:** https://smith.langchain.com

---

**Created:** October 2026  
**Level:** Beginner  
**Time to complete:** 2-3 hours

Happy learning! 🚀
