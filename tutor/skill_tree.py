import json
from pathlib import Path

SKILL_TREE_FILE = "skill_tree.json"

def load_skill_tree() -> dict:
    """Load skill tree from disk or create a fresh one."""
    if Path(SKILL_TREE_FILE).exists():
        with open(SKILL_TREE_FILE, "r") as f:
            return json.load(f)
    return {
        "concepts_seen": [],
        "concepts_mastered": [],
        "questions_asked": 0,
        "correct_answers": 0,
        "papers_studied": []
    }

def save_skill_tree(tree: dict):
    """Save skill tree to disk."""
    with open(SKILL_TREE_FILE, "w") as f:
        json.dump(tree, f, indent=2)

def mark_concept_seen(tree: dict, concept: str) -> dict:
    """Mark a concept as seen."""
    if concept not in tree["concepts_seen"]:
        tree["concepts_seen"].append(concept)
    save_skill_tree(tree)
    return tree

def mark_concept_mastered(tree: dict, concept: str) -> dict:
    """Mark a concept as mastered."""
    if concept not in tree["concepts_mastered"]:
        tree["concepts_mastered"].append(concept)
    if concept not in tree["concepts_seen"]:
        tree["concepts_seen"].append(concept)
    save_skill_tree(tree)
    return tree

def add_paper(tree: dict, paper_title: str) -> dict:
    """Add a paper to the studied list."""
    if paper_title not in tree["papers_studied"]:
        tree["papers_studied"].append(paper_title)
    save_skill_tree(tree)
    return tree

def record_answer(tree: dict, correct: bool) -> dict:
    """Record a question attempt."""
    tree["questions_asked"] += 1
    if correct:
        tree["correct_answers"] += 1
    save_skill_tree(tree)
    return tree

def get_progress(tree: dict) -> str:
    """Return a formatted progress summary."""
    total_q = tree["questions_asked"]
    correct = tree["correct_answers"]
    score = f"{correct}/{total_q}" if total_q > 0 else "0/0"
    accuracy = f"{correct/total_q:.0%}" if total_q > 0 else "N/A"

    return (
        f"Papers studied: {len(tree['papers_studied'])}\n"
        f"Concepts seen: {len(tree['concepts_seen'])}\n"
        f"Concepts mastered: {len(tree['concepts_mastered'])}\n"
        f"Quiz score: {score} ({accuracy})"
    )