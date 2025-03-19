import pytest
from pubmed_fetcher import fetch_pubmed_ids, fetch_paper_details

def test_fetch_pubmed_ids():
    """Test if the function returns a list of PubMed IDs."""
    query = "cancer research"
    pubmed_ids = fetch_pubmed_ids(query)
    
    assert isinstance(pubmed_ids, list), "Expected a list of PubMed IDs"
    assert len(pubmed_ids) > 0, "Expected at least one PubMed ID"

def test_fetch_paper_details():
    """Test if the function correctly fetches details for a given PubMed ID."""
    sample_ids = ["12345678", "87654321"]  # Example PubMed IDs
    papers = fetch_paper_details(sample_ids)
    
    assert isinstance(papers, list), "Expected a list of paper details"
    if papers:
        assert "PubmedID" in papers[0], "Missing PubmedID in results"
        assert "Title" in papers[0], "Missing Title in results"
        assert "Publication Date" in papers[0], "Missing Publication Date"

def test_filtering_logic():
    """Test if filtering correctly excludes academic authors."""
    sample_ids = ["12345678"]
    papers = fetch_paper_details(sample_ids)

    for paper in papers:
        assert paper["Non-academic Author(s)"] != "N/A", "Academic-only papers should be filtered out"
