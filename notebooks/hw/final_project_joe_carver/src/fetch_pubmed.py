from Bio import Entrez
import pandas as pd
from pathlib import Path
import time

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = REPO_ROOT / 'data' / 'raw'
MAX_RESULTS = 2000
PUBLICATIONS = ['Nature', 'Cell']
START = 2000
END = 2026

# ---------------------------------------------------------------
# get citations from pubmed using biopython entrez functionality
# ---------------------------------------------------------------

def get_scientific_citations(journal_name, year, max_results=5):
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
    
    try:
        # 1. Search for IDs using the filtered query
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        pmid_list = search_results["IdList"]
        if not pmid_list:
            print("No matching peer-reviewed articles found.")
            return
        
        #print(f"Found {len(pmid_list)} articles. Fetching XML data.")

        # 2. Fetch data in XML format
        fetch_handle = Entrez.efetch(db="pubmed", id=pmid_list, retmode="xml")
        xml_data = Entrez.read(fetch_handle)
        fetch_handle.close()
        
        # 3. Build dataframe from XML
        authors = []
        pub_info = []
        for article in xml_data['PubmedArticle']:
            medline_citation = article['MedlineCitation']
            pmid = medline_citation['PMID']
            title = medline_citation['Article']['ArticleTitle']
            
            # get publication type
            pub_type_names =medline_citation['Article'].get('PublicationTypeList', [])
            if not pub_type_names:
                continue

            # get mesh terms
            mesh_list = medline_citation.get('MeshHeadingList', [])
            mesh_terms = []
            for mesh in mesh_list:
                term = str(mesh['DescriptorName'])
                mesh_terms.append(term)

            # get funding sources
            grants = medline_citation['Article'].get('GrantList', [])
            grant_ids = []
            funding_agency = []
            funding_country = []
            for grant in grants:
                grant_id = grant.get('GrantID', 'unknown_ID')
                agency = grant.get('Agency', 'unknown_agency') 
                country = grant.get('Country', 'unknown_country')
                grant_ids.append(grant_id)
                funding_agency.append(agency)
                funding_country.append(country)

            pub_info.append({
                "pmid": pmid,
                "journal": journal_name,
                "title": title,
                "year": year,
                "pub_types": '|'.join(pub_type_names),
                "mesh_terms":"|".join(mesh_terms),
                "grant_ids": "|".join(grant_ids),
                "funding_agencies": "|".join(funding_agency),
                "funding_country": "|".join(funding_country)
            })
            
            # get authors and affiliations
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

                    authors.append({
                        "PMID": pmid,
                        'year': year,
                        "author": author_name if author_name else None,
                        "affiliations": "|".join(affiliations) if affiliations else "No affiliation"
                        })
            else:
                continue
                
        pubs = pd.DataFrame(pub_info)
        authors = pd.DataFrame(authors)
        #print(f"Retrieved {len(pubs['title'].unique())} publications with {len(authors['author'])} authors from {journal_name} in {year}")

        return pubs, authors

    except Exception as e:
        print(f"An error occurred during the xml fetch: {e}")

def run():
    for publication in PUBLICATIONS:

        all_authors = []
        all_pubs = []
        error_years = []

        for year in range(START,END+1):
            time.sleep(1)
            try:
                pubs, authors = get_scientific_citations(journal_name = publication, year = year, max_results= MAX_RESULTS)
                all_pubs.append(pubs)
                all_authors.append(authors)
            except Exception as e:
                error_years.append(year)
                print(f"An error occured during the main loop during year {year} processing: {e}")

        final_pubs = pd.concat(all_pubs)
        final_authors = pd.concat(all_authors)
        csv_name_pub = f"{publication}_{START}-{END}_pub_info.csv"
        csv_name_author = f"{publication}_{START}-{END}_author_info.csv"
        final_pubs.to_csv(RAW_DATA_DIR / csv_name_pub)
        final_authors.to_csv(RAW_DATA_DIR / csv_name_author)
        print(f'done fetching {publication} pubmed data')
        if len(error_years) >0:
            print(f'errors occurred during years: {error_years}. Recommend re-running.')
        else:
            print(f"no errors occurred. {len(final_authors)} authors retrieved from {len(final_pubs)} publications")

if __name__ == "__main__":
    run()
    # all_authors = []
    # all_pubs = []

    # for year in range(2000,2026):
    #     time.sleep(2)
    #     try:
    #         pubs, authors = get_scientific_citations(journal_name = "Nature", year = year, max_results= MAX_RESULTS)
    #         all_pubs.append(pubs)
    #         all_authors.append(authors)
    #     except Exception as e:
    #         print(f"An error occured during the main loop during year {year} processing: {e}")

    # final_pubs = pd.concat(all_pubs)
    # final_authors = pd.concat(all_authors)
    # csv_name_pub = f"Nature_2000-2026_pub_info.csv"
    # csv_name_author = f"Nature_2000-2026_author_info.csv"
    # final_pubs.to_csv(RAW_DATA_DIR / csv_name_pub)
    # final_authors.to_csv(RAW_DATA_DIR / csv_name_author)


