import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

print("=== LangSmith Configuration ===")
print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_API_KEY set: {bool(os.getenv('LANGCHAIN_API_KEY'))}")
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
print("================================\n")

def main():
    information = """Elon Reeve Musk is a business magnate and investor. He is the founder, CEO and chief engineer of SpaceX;
angel investor, CEO and product architect of Tesla, Inc.; owner and 'Chief Twit' of Twitter;
founder of The Boring Company; co-founder of Neuralink and OpenAI; and president of the Musk Foundation."""

    summary_template = """
given the information {information} about a person I want you to create:
1. A short summary
2. two interesting facts about them
"""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information})
    print(response.content)

if __name__ == "__main__":
    main()
