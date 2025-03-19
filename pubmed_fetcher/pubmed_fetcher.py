import requests
import pandas as pd
import xml.etree.ElementTree as ET  # ✅ Import ElementTree properly
from typing import List, Dict


PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
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
    print("✅ Function Started: fetch_paper_details()")

    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get(PUBMED_DETAILS_URL, params=params)
        response.raise_for_status()

        # ✅ Print the API Response for debugging
        print(f"📄 API Response for {pmid} (First 500 chars):\n{response.text[:500]}\n")

        # ✅ Save response for manual verification
        with open(f"debug_{pmid}.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        # ✅ Fix: Ensure `ET` is imported correctly
        import xml.etree.ElementTree as ET  

        try:
            root = ET.fromstring(response.text)  # ✅ Proper XML Parsing
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        # Extract Title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        # Extract Publication Date
        pub_date_element = root.find(".//PubDate/Year")
        pub_date = pub_date_element.text if pub_date_element is not None else "Unknown"

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "TBD",
            "Company Affiliation(s)": "TBD",
            "Corresponding Author Email": "TBD"
        })

    return papers

    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    print("✅ Function Started: fetch_paper_details()")

    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
        response.raise_for_status()

        print(f"📄 API Response Received for {pmid} (First 500 chars): {response.text[:500]}")

        # ✅ Save XML response for debugging
        with open(f"debug_{pmid}.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        # ✅ Fix: Ensure `ET` is referenced correctly before using it
        try:
            root = ET.fromstring(response.text)  # ✅ Proper XML Parsing
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        # Extract Title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        # Extract Publication Date
        pub_date_element = root.find(".//PubDate/Year")
        pub_date = pub_date_element.text if pub_date_element is not None else "Unknown"

        # Extract Authors & Affiliations
        non_academic_authors = []
        company_affiliations = []

        for author in root.findall(".//Author"):
            name = author.find("LastName")
            name_text = name.text if name is not None else "Unknown"

            affiliation = author.find(".//Affiliation")
            affiliation_text = affiliation.text.lower() if affiliation is not None else ""

            if any(word in affiliation_text for word in ["inc", "pharma", "biotech", "corp", "ltd", "gmbh", "s.a.", "therapeutics", "biosciences"]):
                non_academic_authors.append(name_text)
                company_affiliations.append(affiliation_text)

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "None",
            "Corresponding Author Email": "Unknown"  # You may need to extract this separately
        })

    return papers

    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    print("✅ Function Started: fetch_paper_details()")
    
    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
        response.raise_for_status()

        print(f"📄 API Response Received for {pmid} (First 500 chars): {response.text[:500]}")

        # ✅ DEBUG: Save XML response to check manually
        with open(f"debug_{pmid}.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        # ✅ FIX: Make sure ET is being referenced correctly before using it
        try:
            root = ET.fromstring(response.text)  # ✅ Fix XML Parsing
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        # Extract Title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        # Extract Publication Date
        pub_date_element = root.find(".//PubDate/Year")
        pub_date = pub_date_element.text if pub_date_element is not None else "Unknown"

        # Extract Authors & Affiliations
        non_academic_authors = []
        company_affiliations = []

        for author in root.findall(".//Author"):
            name = author.find("LastName")
            name_text = name.text if name is not None else "Unknown"

            affiliation = author.find(".//Affiliation")
            affiliation_text = affiliation.text.lower() if affiliation is not None else ""

            if any(word in affiliation_text for word in ["inc", "pharma", "biotech", "corp", "ltd", "gmbh", "s.a.", "therapeutics", "biosciences"]):
                non_academic_authors.append(name_text)
                company_affiliations.append(affiliation_text)

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "None",
            "Corresponding Author Email": "Unknown"  # You may need to extract this separately
        })

    return papers
    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    print("✅ Function Started: fetch_paper_details()")
    
    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
        response.raise_for_status()

        print(f"📄 API Response Received for {pmid} (First 500 chars): {response.text[:500]}")

        # ✅ DEBUG: Save response to a file to manually check XML structure
        with open(f"debug_{pmid}.xml", "w", encoding="utf-8") as f:
            f.write(response.text)

        try:
            root = ET.fromstring(response.text)  # ✅ Fix XML Parsing
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        # Extract Title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        # Extract Publication Date
        pub_date_element = root.find(".//PubDate")
        pub_date = pub_date_element.text if pub_date_element is not None else "Unknown"

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "Unknown",  # Update this logic later
            "Company Affiliation(s)": "Unknown",  # Update this logic later
            "Corresponding Author Email": "Unknown"
        })

    return papers
    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    print("✅ Function Started: fetch_paper_details()")
    
    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
        response.raise_for_status()

        print(f"📄 API Response Received for {pmid} (First 500 chars): {response.text[:500]}")

        try:
            root = ET.ElementTree(ET.fromstring(response.text))  # ✅ Fix XML Parsing
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        # Extract Title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        # Extract Publication Date
        pub_date_element = root.find(".//PubDate")
        pub_date = pub_date_element.text if pub_date_element is not None else "Unknown"

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "Unknown",  # Update this logic later
            "Company Affiliation(s)": "Unknown",  # Update this logic later
            "Corresponding Author Email": "Unknown"
        })

    return papers
    """Fetch details for a list of PubMed IDs and filter papers with non-academic authors."""
    print("✅ Function Started: fetch_paper_details()")
    
    papers = []

    for pmid in pubmed_ids:
        print(f"📌 Fetching details for PubMed ID: {pmid}")

        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml"
        }
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
        response.raise_for_status()

        print(f"📄 API Response Received for {pmid} (First 500 chars): {response.text[:500]}")

        try:
            root = ET.ElementTree(ET.fromstring(response.text))  # ✅ Debug here
            print(f"✅ XML Parsed Successfully for PubMed ID: {pmid}")
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

    return papers
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

        try:
            # ✅ Fix: Explicitly use `ET` inside the function
            root = ET.ElementTree(ET.fromstring(response.text))
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for PubMed ID {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        title = root.find(".//ArticleTitle")
        title = title.text if title is not None else "Unknown"

        pub_date = root.find(".//PubDate")
        pub_date = pub_date.text if pub_date is not None else "Unknown"

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "Unknown"

        for author in root.findall(".//Author"):
            name = author.find("LastName")
            name = name.text if name is not None else "Unknown"

            affiliation = author.find(".//Affiliation")
            affiliation = affiliation.text if affiliation is not None else ""

            email = author.find(".//ElectronicAddress")
            if email is not None:
                corresponding_email = email.text

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
                "Corresponding Author Email": corresponding_email
            })

    return papers
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

        try:
            root = ET.fromstring(response.text)  # ✅ Ensure XML is parsed correctly
        except ET.ParseError as e:
            print(f"❌ XML Parsing Error for PubMed ID {pmid}: {e}")
            continue  # Skip this PubMed ID if XML is broken

        title = root.find(".//ArticleTitle").text if root.find(".//ArticleTitle") is not None else "Unknown"
        pub_date = root.find(".//PubDate").text if root.find(".//PubDate") is not None else "Unknown"

        non_academic_authors = []
        company_affiliations = []

        for author in root.findall(".//Author"):
            name = author.find("LastName").text if author.find("LastName") is not None else "Unknown"
            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else ""

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
            "retmode": "xml"
        }
        response = requests.get(PUBMED_DETAILS_URL, params=params)
        response.raise_for_status()

        # ✅ FIX: Ensure XML parsing is done properly
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            print(f"❌ Error parsing XML for PubMed ID {pmid}: {e}")
            continue

        title = root.find(".//ArticleTitle").text if root.find(".//ArticleTitle") is not None else "Unknown"
        pub_date = root.find(".//PubDate").text if root.find(".//PubDate") is not None else "Unknown"

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "Unknown"

        for author in root.findall(".//Author"):
            name = author.find("LastName").text if author.find("LastName") is not None else "Unknown"
            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else ""

            email = author.find(".//ElectronicAddress")
            if email is not None:
                corresponding_email = email.text

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
                "Corresponding Author Email": corresponding_email
            })

    return papers
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
    df.to_csv(filename, index=False, encoding="utf-8-sig")

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

