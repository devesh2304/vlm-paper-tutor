# VLM Research Paper Tutor

An AI-powered research paper tutor that ingests PDFs and teaches their
content actively through explanation, quizzing, and skill tracking.

## What it does

Drop in any research paper PDF. The tutor parses it — including sections,
figures, and tables — embeds it into a vector database, and becomes your
personal teacher for that paper. Ask questions, take quizzes, and track
your understanding through a persistent skill tree.

## Architecture
```
PDF Input
    ↓
Docling (extract sections + figures + tables)
    ↓
Sentence Transformers (embed chunks)
    ↓
Qdrant (vector storage + similarity search)
    ↓
Groq LLM (explain + quiz + check answers)
    ↓
Skill Tree (track concepts seen + mastered)
```

## Features

- Parses research PDFs including figures and tables via Docling
- Embeds content into Qdrant vector database for semantic search
- Explains concepts using only content from the paper
- Generates multiple choice quizzes on any topic
- Checks answers and provides detailed feedback
- Persistent skill tree tracking concepts seen and mastered
- Quiz score tracking across sessions

## Installation
```bash
git clone https://github.com/devesh2304/vlm-paper-tutor
cd vlm-paper-tutor
python3 -m venv env && source env/bin/activate
pip install docling qdrant-client langchain-groq ragas python-dotenv rich sentence-transformers
```

## Setup

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at console.groq.com

## Usage
```bash
python3 main.py
```

When prompted, enter the path to your PDF:
```
Enter path to your PDF paper: papers/your_paper.pdf
```

Then choose from:
- **1** — Ask a question about the paper
- **2** — Take a quiz on a topic
- **3** — View your skill tree
- **4** — Exit

## Example

Tested on the Attention Is All You Need paper (Vaswani et al., 2017).
The tutor correctly explained the attention mechanism, referenced Figure 2
and Section 3.2, and generated accurate multiple choice questions.

## Stack

- Python · Docling · Qdrant · Sentence Transformers · LangChain · Groq API · Rich