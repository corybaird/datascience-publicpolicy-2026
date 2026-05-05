---

## Dataset Details

### Central Bank Communications

#### Central Banker Speeches (CBS)
*   **Description:** A massive collection of speeches delivered by senior officials from central banks globally, sourced from the Bank for International Settlements (BIS).
*   **Scale:** 19,300+ speeches covering 118 countries.
*   **Temporal Coverage:** 1997 – 2025.
*   **Key Features:** Includes full speech text, central bank identifier, date, and metadata. Primarily used for NLP research in economics to track policy discourse and market sentiment.
*   **Source:** [samchain/bis_central_bank_speeches](https://huggingface.co/datasets/samchain/bis_central_bank_speeches) (Scraped from BIS.org).

#### World Central Bank (WCB) - 380k Sentences
*   **Description:** A unified framework corpus for deciphering global central bank communications.
*   **Scale:** 380,200 sentences from 25 central banks.
*   **Key Features:** Contains an annotated subset of 25,000 sentences labeled for **Stance Detection** (Hawkish/Dovish), **Temporal Classification** (Forward-looking), and **Uncertainty Estimation**.
*   **Source:** [gtfintechlab/WCB_380k_sentences](https://huggingface.co/datasets/gtfintechlab/WCB_380k_sentences).

#### FOMC Corpus
*   **Description:** Specialized dataset focusing on the Federal Open Market Committee (FOMC) of the U.S. Federal Reserve.
*   **Content:** Meeting transcripts, statements, and materials covering inflation, labor markets, and monetary policy outlooks.
*   **Source:** [gtfintechlab/fomc_communication](https://huggingface.co/datasets/gtfintechlab/fomc_communication).

#### CentralBankRoBERTa Labels
*   **Description:** Model-generated labels specifically for central bank communications.
*   **Key Features:** Classifies sentiment and identifies economic agents (Households, Firms, Financial Sector, Government) influenced by central bank statements.
*   **Source:** Based on the work by Moritz Pfeifer.

### News & Media


#### RSS Scraper Live Feed
*   **Description:** A continuously updating stream of news articles from global sources (BBC, NYT, Al Jazeera, Reuters, etc.).
*   **Automation:** Runs hourly via macOS `launchd`.
*   **Content:** Real-time headlines and descriptions for global events.
*   **Storage:** Aggregated into Parquet files for time-series analysis.

#### US Public Domain Newspapers
*   **Description:** Digitized periodicals from the Library of Congress (*Chronicling America*).
*   **Temporal Coverage:** 1690 – 1963.
*   **Scale:** 21 million editions, nearly 100 billion words.
*   **Key Features:** Public domain OCR text used for historical research, language modeling, and studying political polarization over centuries.
*   **Source:** [PleIAs/US-PD-Newspapers](https://huggingface.co/datasets/PleIAs/US-PD-Newspapers).

### Political & Parliamentary Data

#### ParlGov (Parliaments and Governments)
*   **Description:** Data infrastructure for the empirical study of parties, elections, and governments.
*   **Coverage:** EU and OECD member countries (Post-war period).
*   **Key Features:** Tracks **Cabinet-level transitions**, **Election results** (vote shares, seats), and **Party positions** (left-right scales).
*   **Source:** [parlgov.org](https://www.parlgov.org).

#### Comparative Agendas Project (CAP)
*   **Description:** Tracks government policy activity across time using a universal coding scheme for bills, laws, and media.
*   **Scale:** 147 datasets across multiple topics (budgets, hearings, legislation).
*   **Key Features:** Uses a standardized set of major topic codes to track policy attention and legislative output across decades.
*   **Source:** [comparativeagendas.net](https://www.comparativeagendas.net).

#### CLARIN Parliamentary Corpora
*   **Description:** Interoperable parliamentary debates (ParlaMint project) across 29+ European countries.
*   **Key Features:** Richly annotated with POS-tagging, lemmatization, and speaker metadata (party, gender).
*   **Source:** [clarin.eu](https://www.clarin.eu).

### Planned / Pending Datasets

#### ParlLawSpeech
*   **Description:** A massive collection of legislative process documents, linking plenary speeches to the specific bills and laws they discuss.
*   **Scale:** 3M+ speeches, 40,000+ bills, and 28,000+ laws across 8 European entities.
*   **Status:** Pending download.
*   **Key Features:** Uses a unique `procedure_ID` to track the lifecycle of a law from proposal to adoption.

#### ParlSpeech V2
*   **Description:** Full-text corpora of parliamentary speeches from 9 major democracies (UK, Germany, Spain, etc.).
*   **Scale:** 6.3 million speeches.
*   **Temporal Coverage:** ~30 years of legislative discourse.
*   **Status:** Pending download.

#### ParlText CEE
*   **Description:** Specialized dataset for Central-Eastern Europe, covering the Visegrád countries (Czechia, Hungary, Poland, Slovakia).
*   **Scale:** 2.3 million text vectors.
*   **Temporal Coverage:** 1990 – 2024 (Post-democratic transition).
*   **Status:** Pending download.

#### EconLit & NBER Public Use Archive
*   **Description:** Bibliographic and full-text data from the American Economic Association (AEA) and National Bureau of Economic Research (NBER).
*   **Content:** 15k+ econ papers and 30k+ NBER working papers.
*   **Key Features:** Focuses on economic research trends, JEL classification codes, and high-quality economic/demographic text.
*   **Status:** Pending pipeline implementation.

---