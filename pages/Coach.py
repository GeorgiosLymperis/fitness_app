import streamlit as st

from ai.rag import FitnessRAG
from ai.tools import FitnessTools
from ai.agents import fitness_agent
from ai.llm import FitnessLLM

st.set_page_config(page_title="Coach", layout="centered")
st.title("Coach")

with st.form("form"):
    backend = st.selectbox(
        "Select inference backend",
        ["Local LLM", "SmolAgent (Hugging Face API)"]
    )
    question = st.text_input("Question")
    submit = st.form_submit_button("Submit")

def fitness_rag():
    return FitnessRAG([
        "utils/data/weight_standards.csv",
        "utils/data/bodyweight_standards.csv",
        "utils/diet_rules.md",
        "utils/coaching_rules.md",
    ])


PROMPT_TEMPLATE = """
You are a fitness trainer.

Question:
{question}

Answer:
"""


# -----------------------------
# Initialization
# -----------------------------
rag = fitness_rag()
tools = FitnessTools(rag)
agent = fitness_agent(tools)
local_llm = FitnessLLM()


# -----------------------------
# Inference
# -----------------------------
if submit and question:
    context_chunks = rag.retrieve(question, k=3)
    context = "\n".join(context_chunks)

    prompt = PROMPT_TEMPLATE.format(
        question=question
    )

    with st.spinner("Generating answer..."):
        if backend == "Local LLM":
            answer = local_llm.generate(prompt).content
        else:
            prompt = """

            You are a fitness trainer.

            Question:
            {question}

            Answer:
            """.format(
                question=question
            )
            answer = agent.run(prompt)

    st.subheader("Answer")
    st.write(answer)
