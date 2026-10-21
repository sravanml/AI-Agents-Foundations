# Chapter 2: Your First Agent in Action

**What you'll learn:** How agents think and act, building your first agent, integrating real-world tools, and understanding the reasoning loop.

**Time:** 3-4 hours  
**Difficulty:** Intermediate

---

## Table of Contents

1. [Agents vs Chains](#agents-vs-chains)
2. [The ReAct Pattern](#the-react-pattern)
3. [Your First Agent (Mock)](#your-first-agent-mock)
4. [Understanding Tools](#understanding-tools)
5. [Real-World Search (Tavily)](#real-world-search-tavily)
6. [Built-in LangChain Tools](#built-in-langchain-tools)
7. [Structured Output](#structured-output)
8. [Tracing Agent Execution](#tracing-agent-execution)
9. [Summary](#summary)

---

## Agents vs Chains

### Chains (Chapter 1)

You already know chains:

```
Template → LLM → Output (done)
```

**One-shot execution.** The template is filled, sent to LLM, you get a response. Done.

### Agents (Chapter 2)

Agents are different:

```
LLM thinks → Decides which tool to use → Executes tool → 
Sees result → Thinks again → Gives final answer
```

**Loop-based execution.** The agent can **reason**, **act**, **observe**, then **reason again**.

### Example: Summarizing vs Researching

**Chain approach:**
```
"Summarize the weather in Tokyo"
→ LLM thinks about what it knows
→ Returns summary from training data
```

**Agent approach:**
```
"What's the weather in Tokyo?"
→ LLM thinks: "I need current data, I'll use the search tool"
→ Calls search tool → Gets real data
→ LLM thinks: "Now I have real data, let me answer"
→ Returns answer with current information
```

**Key difference:** Agents can **use external tools** to get information.

---

## The ReAct Pattern

ReAct = **Reasoning + Acting**

The agent loops through:

1. **Reason** — "What do I need to do?"
2. **Act** — "I'll call this tool"
3. **Observe** — "Here's what the tool returned"
4. Repeat until done

### Visual Flow

```
User: "What's the weather in Tokyo?"
         ↓
    LLM (Reason)
    "I need current weather, I'll search"
         ↓
    Tool Call: search("weather in Tokyo")
         ↓
    Tool Returns: "Tokyo: 16°C, sunny"
         ↓
    LLM (Reason again)
    "I have the data, time to answer"
         ↓
    Final Answer: "It's 16°C and sunny in Tokyo"
```

### Why This Matters

- **Chains can't adapt** — They always do the same thing
- **Agents can adapt** — They decide what to do based on the question
- **Agents can use multiple tools** — They pick the right tool for each task
- **Agents can iterate** — They can call tools multiple times if needed

---

## Summary

**You learned:**
- ✅ Difference between chains and agents
- ✅ The ReAct pattern
- ✅ How agents reason and act
- ✅ When to use agents vs chains

**Next:** See the code in agent_examples.py

