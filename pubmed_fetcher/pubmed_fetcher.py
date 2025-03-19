import requests
import pandas as pd
import re
from typing import List, Dict

print("Imports successful. Now executing main logic...")

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


# Define keywords to detect companies and filter out universities
COMPANY_KEYWORDS = ["inc", "pharma", "biotech", "corp", "ltd", "gmbh", "s.a.", "research institute", "therapeutics", "biosciences"]
ACADEMIC_KEYWORDS = ["university", "college", "school", "institute of technology", "hospital", "med school"]

def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch PubMed IDs based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "retmode": "json"
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    papers = []

    for pmid in pubmed_ids:
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get(PUBMED_DETAILS_URL, params=params)
        response.raise_for_status()
        
        # 🔍 Print response text for debugging
        print(f"Response for {pmid}: {response.text[:500]}...")  # Print first 500 chars

        # Parse XML response (PubMed provides affiliations in XML format)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.text)

        title = root.find(".//ArticleTitle").text if root.find(".//ArticleTitle") is not None else "Unknown"
        pub_date = root.find(".//PubDate").text if root.find(".//PubDate") is not None else "Unknown"
        
        non_academic_authors = []
        company_affiliations = []

        for author in root.findall(".//Author"):
            name = author.find("LastName").text if author.find("LastName") is not None else "Unknown"
            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else ""

            print(f"Author: {name}, Affiliation: {affiliation}")

            # Check if affiliation belongs to a company
            if any(word in affiliation.lower() for word in COMPANY_KEYWORDS) and not any(word in affiliation.lower() for word in ACADEMIC_KEYWORDS):
                non_academic_authors.append(name)
                company_affiliations.append(affiliation)

        if non_academic_authors:
            papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": "Unknown"
            })

    return papers

    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    papers = []
    
    for pmid in pubmed_ids:
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "json"
        }
        response = requests.get(PUBMED_SUMMARY_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 🔍 Print the full response to understand its structure
        print(f"Response for {pmid}: {data}")

        paper_info = data.get("result", {}).get(pmid, {})

        title = paper_info.get("title", "Unknown")
        pub_date = paper_info.get("pubdate", "Unknown")
        authors = paper_info.get("authors", [])

        non_academic_authors = []
        company_affiliations = []

        for author in authors:
            if "affiliation" in author:
                affiliation = author["affiliation"].lower()

                # Check if the affiliation is a company
                if any(word in affiliation for word in COMPANY_KEYWORDS) and not any(word in affiliation for word in ACADEMIC_KEYWORDS):
                    non_academic_authors.append(author["name"])
                    company_affiliations.append(affiliation)

        # **Filter out papers without non-academic authors**
        if non_academic_authors:
            papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": "Unknown"
            })

    return papers

    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    papers = []
    
    for pmid in pubmed_ids:
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "json"
        }
        response = requests.get(PUBMED_SUMMARY_URL, params=params)
        response.raise_for_status()
        data = response.json()
        paper_info = data.get("result", {}).get(pmid, {})

        title = paper_info.get("title", "Unknown")
        pub_date = paper_info.get("pubdate", "Unknown")
        authors = paper_info.get("authors", [])

        non_academic_authors = []
        company_affiliations = []

        for author in authors:
            if "affiliation" in author:
                affiliation = author["affiliation"].lower()

                # Check if the affiliation is a company
                if any(word in affiliation for word in COMPANY_KEYWORDS) and not any(word in affiliation for word in ACADEMIC_KEYWORDS):
                    non_academic_authors.append(author["name"])
                    company_affiliations.append(affiliation)

        # **Filter out papers without non-academic authors**
        if non_academic_authors:
            papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": "Unknown"
            })
    
    return papers

def save_to_csv(papers: List[Dict], filename: str):
    """Save fetched paper details to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)

def main():
    print("Fetching PubMed IDs...")
    query = "biotechnology"  # Example query, replace with user input if needed
    pubmed_ids = fetch_pubmed_ids(query)
    print(f"Fetched {len(pubmed_ids)} PubMed IDs:", pubmed_ids)

    print("Fetching paper details...")
    papers = fetch_paper_details(pubmed_ids)
    print(f"Fetched {len(papers)} papers with non-academic authors.")

    if papers:
        filename = "papers.csv"
        save_to_csv(papers, filename)
        print(f"Results saved to {filename}.")
    else:
        print("No papers found with non-academic authors.")

# Ensure script runs when executed directly
if __name__ == "__main__":
    main()

