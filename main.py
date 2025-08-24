from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2-vision:11b")

template = """
You are a AI 
Make sure you output as short as you can

here is the question to answer : {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model 

while True:
    print("\n-------------------------------------------------------------\n")
    question = input("what is your question\n")
    if question == 'q':
        break
    result = chain.invoke({"question": question})
    print(result)