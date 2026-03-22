import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tutor.retriever import retrieve, format_context
from tutor.skill_tree import mark_concept_seen, mark_concept_mastered, record_answer

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def explain_concept(question: str, tree: dict) -> tuple[str, dict]:
    """Retrieve relevant chunks and explain a concept from the paper."""
    chunks = retrieve(question, top_k=5)
    context = format_context(chunks)

    prompt = f"""You are an expert research paper tutor. 
A student is reading a research paper and asked: "{question}"

Here are the most relevant sections from the paper:
{context}

Your job:
1. Give a clear, concise explanation based ONLY on the paper content above
2. Use simple language — assume the student is learning this for the first time
3. Point out which section or figure the explanation comes from
4. End with ONE follow-up question to check understanding

Be conversational and encouraging."""

    response = llm.invoke(prompt)
    answer = response.content

    # extract concept from question and mark as seen
    concept = question[:50].strip()
    tree = mark_concept_seen(tree, concept)

    return answer, tree

def generate_quiz(topic: str, tree: dict) -> tuple[str, dict]:
    """Generate a quiz question about a topic from the paper."""
    chunks = retrieve(topic, top_k=3)
    context = format_context(chunks)

    prompt = f"""You are a research paper tutor creating a quiz.
Based on this content from the paper:
{context}

Generate ONE multiple choice question about "{topic}" with:
- A clear question
- 4 options labeled A, B, C, D
- The correct answer on the last line as: ANSWER: X

Make it challenging but fair."""

    response = llm.invoke(prompt)
    return response.content, tree

def check_answer(question: str, student_answer: str, tree: dict) -> tuple[str, dict]:
    """Check a student's answer and update skill tree."""
    chunks = retrieve(question, top_k=3)
    context = format_context(chunks)

    prompt = f"""You are a research paper tutor checking a student's answer.

Question: {question}
Student's answer: {student_answer}

Relevant paper content:
{context}

Evaluate if the answer is correct based on the paper.
- Say CORRECT or INCORRECT clearly at the start
- Explain why briefly
- If incorrect, give the right answer
- Be encouraging"""

    response = llm.invoke(prompt)
    feedback = response.content

    is_correct = feedback.upper().startswith("CORRECT")
    tree = record_answer(tree, is_correct)

    if is_correct:
        tree = mark_concept_mastered(tree, question[:50])

    return feedback, tree