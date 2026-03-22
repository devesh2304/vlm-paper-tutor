import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from tutor.ingestor import ingest_paper
from tutor.embedder import embed_paper
from tutor.teacher import explain_concept, generate_quiz, check_answer
from tutor.skill_tree import load_skill_tree, get_progress, add_paper

load_dotenv()
console = Console()

def show_progress(tree: dict):
    table = Table(title="Your Skill Tree")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    for line in get_progress(tree).splitlines():
        parts = line.split(": ", 1)
        if len(parts) == 2:
            table.add_row(parts[0], parts[1])
    console.print(table)

def main():
    console.print(Panel(
        "[bold]VLM Research Paper Tutor[/bold]\n"
        "Learn any research paper through active teaching",
        style="cyan"
    ))

    tree = load_skill_tree()

    # load paper
    pdf_path = console.input("\n[bold]Enter path to your PDF paper:[/bold] ").strip()
    if not os.path.exists(pdf_path):
        console.print("[red]File not found. Please check the path.[/red]")
        sys.exit(1)

    with console.status("Ingesting paper..."):
        paper_data = ingest_paper(pdf_path)

    with console.status("Embedding into Qdrant..."):
        embed_paper(paper_data)

    tree = add_paper(tree, paper_data["title"])
    console.print(f"\n[green]✓ Paper loaded:[/green] {paper_data['title']}")
    console.print(f"[dim]{paper_data['total_sections']} sections · "
                  f"{paper_data['total_figures']} figures · "
                  f"{paper_data['total_tables']} tables[/dim]\n")

    # main loop
    while True:
        console.print(
            "\n[bold]What would you like to do?[/bold]\n"
            "  [cyan]1[/cyan] — Ask a question about the paper\n"
            "  [cyan]2[/cyan] — Take a quiz on a topic\n"
            "  [cyan]3[/cyan] — View my skill tree\n"
            "  [cyan]4[/cyan] — Exit"
        )

        choice = console.input("\n[bold cyan]Choice:[/bold cyan] ").strip()

        if choice == "1":
            question = console.input("[bold]Your question:[/bold] ").strip()
            with console.status("Thinking..."):
                answer, tree = explain_concept(question, tree)
            console.print(Panel(answer, style="green", title="Tutor"))

        elif choice == "2":
            topic = console.input("[bold]Topic to quiz on:[/bold] ").strip()
            with console.status("Generating quiz..."):
                quiz, tree = generate_quiz(topic, tree)
            console.print(Panel(quiz, style="yellow", title="Quiz"))
            student_answer = console.input("[bold]Your answer (A/B/C/D):[/bold] ").strip()
            with console.status("Checking answer..."):
                feedback, tree = check_answer(quiz, student_answer, tree)
            console.print(Panel(feedback, style="cyan", title="Feedback"))

        elif choice == "3":
            show_progress(tree)

        elif choice == "4":
            show_progress(tree)
            console.print("[dim]Goodbye![/dim]")
            break

        else:
            console.print("[red]Invalid choice, try 1-4[/red]")

if __name__ == "__main__":
    main()