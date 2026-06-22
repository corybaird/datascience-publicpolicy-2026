from Bio import Entrez
# import csv
import pandas as pd
from pathlib import Path
# import git



# ---------------------------------------------------------------
# set up paths
# ---------------------------------------------------------------
# def get_repo_root() -> Path:
#     """
#     Locates the root directory of the current git repository.
#     Returns a pathlib.Path object.
#     """
#     try:
#         git_repo = git.Repo(".", search_parent_directories=True)
#         return Path(git_repo.working_tree_dir).resolve()
#     except git.exc.InvalidGitRepositoryError as e:
#         raise RuntimeError("The current directory is not part of a Git repository") from e

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = REPO_ROOT / 'data' / 'raw'

# ---------------------------------------------------------------
# get citations from pubmed using biopython entrez functionality
# ---------------------------------------------------------------

def get_scientific_citations(journal_name, year, csv_name, max_results=5,):
    Entrez.email = "jocarver@g.ecc.u-tokyo.ac.jp"
    
    # use [PT] (Publication Type) to target core research articles 
    # and explicitly exclude non-peer-reviewed/non-empirical columns.
    query = (
        f'"{journal_name}"[Journal] AND {year}[pdat] '
        f'AND "Journal Article"[PT] '
        f'NOT "Editorial"[PT] '
        f'NOT "Letter"[PT] '
        f'NOT "Comment"[PT] '
        f'NOT "News"[PT] '
        f'NOT "Biography"[PT]'
    )
    
    print(f"Searching PubMed with filters:\n{query}")
    
    try:
        # 1. Search for IDs using the filtered query
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        total_count = int(search_results["Count"])
        if total_count == 0:
            print('No records found')
            return

        
        pmid_list = search_results["IdList"]
        if not pmid_list:
            print("No matching peer-reviewed articles found.")
            return
        
        print(f"Found {len(pmid_list)} articles. Fetching XML data.")

        # 2. Fetch data in XML format
        fetch_handle = Entrez.efetch(db="pubmed", id=pmid_list, retmode="xml")
        xml_data = Entrez.read(fetch_handle)
        fetch_handle.close()
        
        # 3. Build dataframe from XML
        citations = []
        for article in xml_data['PubmedArticle']:
            medline_citation = article['MedlineCitation']
            pmid = medline_citation['PMID']
            title = medline_citation['Article']['ArticleTitle']
            
            # Optional: Grab the Publication Types from the XML to verify it's working
            pub_types = medline_citation['Article']['PublicationTaskList'] if 'PublicationTaskList' in medline_citation['Article'] else []
            pub_type_names = [str(pt) for pt in pub_types]
            
            # print(f"PMID: {pmid}")
            # print(f"TITLE: {title}")
            # print(f"PUB TYPES: {', '.join(pub_type_names)}")
            # print("AUTHORS:")
            
            if 'AuthorList' in medline_citation['Article']:
                author_list = medline_citation['Article']['AuthorList']
                for author in author_list:
                    if 'LastName' in author and 'ForeName' in author:
                        author_name = f"{author['ForeName']} {author['LastName']}"
                    elif 'CollectiveName' in author:
                        author_name = f"{author['CollectiveName']}"
                    else:
                        continue

                    affiliations = []
                    if author.get('AffiliationInfo'):
                        for aff_info in author['AffiliationInfo']:
                            affiliations.append(aff_info['Affiliation'])

                    # Format affiliation string
                    aff_string = " | ".join(affiliations) if affiliations else "No affiliation listed"
                    # print(f"  - {author_name}")
                    # print(f"    Affiliation: {aff_string}")
                    citations.append({
                        "PMID": pmid,
                        "Title": title,
                        "Pub types": '|'.join(pub_type_names),
                        "Author": author_name if author_name else None,
                        "Affiliations": "|".join(affiliations) if affiliations else "No affiliation"

                        })
            else:
                continue
                # print("  No authors listed.")
                
            # print("-" * 50)
        df = pd.DataFrame(citations)
        print(f"Retrieved {len(df['Title'].unique())} publications with {len(df['Author'])} authors.")
        print("Saving XML as output csv")
        df.to_csv(RAW_DATA_DIR / csv_name)


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Test with a journal known for having lots of editorials/news (like Nature)
    get_scientific_citations(journal_name="Nature", year=2024, max_results=1000, csv_name = "pubmed_citations.csv")