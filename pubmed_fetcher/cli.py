import typer
from pubmed_fetcher.pubmed_fetcher import fetch_pubmed_ids, fetch_paper_details, save_to_csv


app = typer.Typer()

@app.command()
def search(
    query: str = typer.Option(..., "--query", "-q", help="Search term for PubMed"),
    file: str = typer.Option(None, "--file", "-f", help="Output file name"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode")
):

    """Fetch and display PubMed papers based on a query, filtering for non-academic authors."""

    typer.echo("✅ Imports successful. Now executing main logic...")

    if debug:
        typer.echo(f"🔍 Searching for: {query}")

    pubmed_ids = fetch_pubmed_ids(query)

    if debug:
        typer.echo(f"📄 Found PubMed IDs: {pubmed_ids}")

    papers = fetch_paper_details(pubmed_ids)

    if not papers:
        typer.echo("❌ No relevant papers found with non-academic authors.")
        return

    if file:
        save_to_csv(papers, file)
        typer.echo(f"✅ Results saved to {file}")
    else:
        typer.echo("📄 Retrieved Papers:")
        for paper in papers:
            typer.echo(paper)


def main():
    app()

if __name__ == "__main__":
    main()
