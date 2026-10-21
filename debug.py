import os
from dotenv import load_dotenv

load_dotenv()

print("=== Environment Variables ===")
print(f"OPENAI_API_KEY exists: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"LANGCHAIN_API_KEY exists: {bool(os.getenv('LANGCHAIN_API_KEY'))}")
print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")

print("\n=== Checking Packages ===")
try:
    import langsmith
    print(f"✓ langsmith installed (version: {langsmith.__version__ if hasattr(langsmith, '__version__') else 'unknown'})")
except ImportError:
    print("✗ langsmith NOT installed")

try:
    import langchain_core
    print("✓ langchain_core installed")
except ImportError:
    print("✗ langchain_core NOT installed")

try:
    import langchain_openai
    print("✓ langchain_openai installed")
except ImportError:
    print("✗ langchain_openai NOT installed")

print("\n=== Running Simple Test ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    template = PromptTemplate(
        input_variables=["name"],
        template="Say hello to {name}"
    )
    chain = template | llm
    result = chain.invoke({"name": "Test"})
    print(f"✓ Chain executed successfully")
    print(f"Response: {result.content[:100]}...")
except Exception as e:
    print(f"✗ Chain failed: {e}")
