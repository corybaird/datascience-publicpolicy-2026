# Student Project Ideas and Dataset Mappings

This document maps student project ideas to existing or planned datasets within our macroeconomic data repository, and suggests external data sources where our coverage might currently be limited.

---

## Group A: AI-Immigration
**Topics:** Immigration related / Immigration statistics and text data

*   **Available Datasets:**
    *   **ILOSTAT (Monthly/Annual):** Extensive labor market indicators which often encompass demographics and labor force structures.
    *   **UN SDG & Demographic Data:** Broad population and sustainable development variables.
    *   **Comparative Agendas Project (CAP):** Contains datasets on immigration-related legislation and bills, useful for tracking policy shifts.
    *   **Multisource Financial News:** Large-scale news archive (10GB+) suitable for sentiment analysis and tracking public discourse on immigration.
    *   **UN Comtrade:** Bilateral trade flows that can proxy for migration-linked economic dependencies.
*   **External Sources to Target:**
    *   Our internal database is structurally light on direct bilateral migration flows. Students should look into the **UN DESA International Migrant Stock** database or **OECD International Migration Database**.

*   **Project Ideas:**
    *   **Media Framing of Immigration Over Time:** Use the Multisource Financial News corpus to track how sentiment and topic framing around immigration shifts across news cycles. Cross-reference with CAP legislative data to test whether media attention precedes or follows policy activity. Can be augmented with GPR or EPU country-specific indices for baseline comparison.
    *   **Immigration Policy and Labor Market Outcomes:** Merge CAP immigration legislation data with ILOSTAT monthly unemployment-by-demographic indicators to assess whether legislative restrictiveness correlates with labor force participation gaps across immigrant-heavy age/sex cohorts. Supplement with OECD International Migration Database for bilateral flow context.
    *   **AI Speech Classifier for Immigration Rhetoric:** Build a supervised classifier that categorizes political speeches on immigration into a structured taxonomy of arguments (economic opportunity, cultural threat, humanitarian, security, fiscal burden). Train on CAP legislative speeches and test cross-country generalizability. Evaluate using F1 scores and confusion matrices to identify which argument categories are most distinguishable vs. ambiguous.
    *   **RAG System for Immigration Policy Research:** Build a Retrieval-Augmented Generation system that answers factual questions about immigration policy by retrieving relevant passages from CAP legislative documents, ILOSTAT reports, and news articles. Quantify retrieval accuracy (hits@3, MRR) and generation quality via human evaluation or GPT-judge.

---

## Group B: AI-Policy
**Topics:** AI Policy and Economic Freedom

*   **Available Datasets:**
    *   **Heritage Economic Freedom Index (EFI):** Annual coverage of economic freedom scores globally.
    *   **Freedom House & V-Dem / Polity5:** Deep institutional quality and civil liberties metrics.
    *   **Comparative Agendas Project (CAP):** Useful for finding legislative hearings and laws related to technology and AI regulation.
*   **External Sources to Target:**
    *   Currently, we don't have dedicated datasets mapping AI policy adoption. Students should cross-reference our economic freedom datasets with the **Stanford AI Index Report**, **Oxford Insights Government AI Readiness Index**, or OECD AI policy observatories.

*   **Project Ideas:**
    *   **Does Economic Freedom Predict AI Regulatory Style?** Combine Heritage EFI scores with Stanford AI Index government strategy data to test whether economically open countries favor lighter-touch AI regulation versus interventionist frameworks. Use V-Dem institutional quality indices as controls. CAP technology hearing counts can serve as a proxy for legislative intensity.
    *   **AI Readiness and Macroeconomic Growth:** Merge the Oxford Insights Government AI Readiness Index with WDI GDP growth, OECD QNA investment data, and Freedom House civil liberties scores to examine whether institutional openness and AI preparedness jointly predict productivity gains.
    *   **AI Policy Speech Taxonomy & Classification:** Collect speeches on AI regulation from CAP technology hearings and build a multi-label classifier that maps speeches onto policy approach categories (precautionary, innovation-friendly, rights-based, industrial strategy). Train a transformer model and analyze which political actors cluster together on each approach.
    *   **RAG System for AI Policy Documents:** Develop a retrieval-augmented QA system that answers questions about AI regulations across countries using the Stanford AI Index, Oxford Insights reports, and news sources. Include citation verification to assess whether the system hallucinates or retrieves accurately.

---

## Group C: Media-Politics
**Topics:** Media, politics, and immigration discourse

*   **Available Datasets:**
    *   **Comparative Agendas Project (CAP):** Includes dedicated datasets mapping media agendas and political topics.
    *   **Multisource Financial News:** Large-scale news archive for analyzing immigration discourse framing.
    *   **Geopolitical Risk Index (GPR):** Daily/Monthly news-based text mining of geopolitical risk factors globally.
    *   **Economic Policy Uncertainty (EPU):** News-based text index tracking policy uncertainty across 25+ countries.
    *   **V-Dem (Varieties of Democracy):** Has specialized modules evaluating media freedom, censorship, and political pluralism.
    *   **RSS Scraper Live Feed:** Real-time global news headlines for monitoring immigration coverage patterns.

*   **Project Ideas:**
    *   **Immigration Narrative Dynamics Across Global Media:** Use the Multisource Financial News corpus to track how immigration is framed (economic opportunity vs. security threat vs. humanitarian crisis) over time. Cross-reference with CAP immigration legislation counts to test whether negative media framing predicts legislative restrictiveness. Supplement with V-Dem media freedom scores to analyze whether framing differs across regime types.
    *   **Media Freedom and Immigration Policy Uncertainty:** Build a cross-country panel using V-Dem media freedom module scores and Freedom House civil liberties data against country-specific EPU indices for immigration-related keywords. Test whether more restricted media environments produce systematically higher or more volatile policy uncertainty signals around immigration.
    *   **Political Speech Taxonomy: Immigration Arguments:** Create a labeled dataset of immigration-related political speeches mapped to argument taxonomies (labor market impact, social cohesion, national security, human rights, economic burden). Use CAP legislative speeches as training data and evaluate classifier performance across countries with different immigration profiles.
    *   **Multilingual RAG for Immigration Policy Research:** Build a cross-lingual retrieval system that answers questions about immigration policy in different countries by pulling from CAP documents, news sources, and government releases. Test retrieval quality across languages (English, German, French, Spanish) using cosine similarity of embeddings and end-to-end QA accuracy.

---

## Group D: Tariffs-Trump-Inflation
**Topics:** Pass-through of 2025 Trump tariffs to US and cross-country consumer prices; trade flow reorientation; spillover effects

*   **Available Datasets:**
    *   **FRED / Cleveland Fed:** Disaggregated US CPI and PCE indicators.
    *   **NY Fed Global Supply Chain Pressure Index (GSCPI):** Proxy for supply chain disruption effects.
    *   **IMF Commodities & OpenBB Commodity Futures:** To track raw material costs prior to manufacturing.
    *   **UN Comtrade:** Bilateral trade flows by HS commodity code to identify which countries and sectors are exposed to US tariff shocks.
    *   **IMF IFS (CPI):** Monthly CPI for 188 countries by COICOP category for cross-country spillover analysis.
    *   **OECD CPI:** Harmonized consumer prices for 34 OECD member states with component breakdowns.
    *   **Eurostat HICP:** Monthly harmonized inflation for 45 EU/EEA member states.
    *   **EPU (Country-Specific):** Policy uncertainty indices for 23 countries to capture tariff-related uncertainty transmission.
*   **External Sources to Target:**
    *   Students will need to acquire highly disaggregated tariff schedules (e.g., from the **USTR** or the **PIIE Trump Tariff Tracker**) and merge these timelines with our disaggregated FRED CPI data.

*   **Project Ideas:**
    *   **Category-Level CPI Pass-Through from Tariff Schedules:** Acquire product-level tariff rates from the USTR or PIIE Tariff Tracker and match to COICOP-level CPI categories from FRED Monthly and Cleveland Fed daily inflation data. Estimate pass-through coefficients by product category using difference-in-differences, with the NY Fed GSCPI controlling for supply chain noise.
    *   **Commodity Costs as a Transmission Channel:** Use OpenBB Commodity Futures (Crude Oil, Copper, Steel proxies) and IMF Commodities monthly indices to model upstream cost pressure before it hits consumer prices. Test whether the GSCPI or commodity price spike mediates the tariff-to-CPI relationship, isolating the supply-chain channel from the direct price effect.
    *   **Cross-Country Inflation Spillover from US Tariffs:** Use UN Comtrade bilateral trade flows to identify which countries export tariff-affected products to the US. Then use IMF IFS (188 countries) and OECD CPI (34 countries) to test whether tariff shocks to one country generate measurable inflation pressure in exporting partner countries. Apply local projection methods or SVAR to estimate impulse responses of CPI to tariff shocks across the trade network.
    *   **Trade Flow Reorientation and Third-Country Effects:** Track how UN Comtrade bilateral trade flows shift after tariff introduction—do affected exporters reroute through third countries to avoid US tariffs? Use IMF IFS CPI and Eurostat HICP to test whether trade diversion generates inflation spillover in third markets not directly targeted by tariffs but embedded in supply chains.
    *   **Media Sentiment as an Early Warning Indicator for Tariff Escalation:** Train a sentiment classifier on Multisource Financial News articles mentioning tariffs to generate a daily "trade tension" signal. Test whether this signal leads movements in affected commodity futures (steel, aluminum, soybeans) and whether it improves nowcasting models for CPI pass-through timing.
    *   **RAG System for US Trade Policy Research:** Build a retrieval-augmented system that answers questions about tariff history, affected product categories, and expected CPI impact by retrieving from USTR announcements, news articles, and FRED commentary. Include a hallucination detection module that cross-checks claims against source documents.

---

## Group G: Tech-Development
**Topics:** International Organizations Data, Tech industry development & semiconductors, Developmental states

*   **Available Datasets:**
    *   **World Bank WDI / IMF (BOP, GFS, etc.) / OECD QNA:** Deep historical tracking of government spending and economic structural balances.
    *   **Comparative Agendas Project (CAP):** Datasets on government budgets and laws related to industrial policy and technological development.
    *   **SWIID (Standardized World Income Inequality Database):** Ideal for social policy tracking.
    *   **Bruegel European Clean Tech Tracker:** (Planned) Useful for tracking early iterations of high-tech manufacturing policies.
*   **External Sources to Target:**
    *   For semiconductors, specific data from the **Semiconductor Industry Association (SIA)** or tech-specific trade volume APIs might be necessary to augment the UN Comtrade data we have.

*   **Project Ideas:**
    *   **Industrial Policy Spending and Tech Export Complexity:** Use IMF GFS government expenditure data and CAP industrial policy legislation counts to build a panel measuring state intervention intensity. Merge with UN Comtrade bilateral trade flows (HS codes for electronics/semiconductors) to test whether directed spending shifts export composition toward high-tech goods. Supplement with SIA semiconductor shipment data.
    *   **Developmental State Models and Inequality Outcomes:** Combine WDI GDP per capita, OECD QNA investment shares, and IMF BOP FDI data to classify countries by developmental state characteristics. Cross-reference with SWIID Gini (disposable vs. market income) to assess whether industrial-policy-heavy states reduced inequality more than liberal market economies over comparable development windows.
    *   **Speech-Based Classification of Industrial Policy Arguments:** Build a classifier that maps legislative speeches on industrial policy to argument categories (national security, economic growth, job creation, technology transfer, strategic competition). Use CAP data to train and evaluate with stratified cross-validation. Analyze temporal trends in which argument types dominate across countries.
    *   **RAG System for Tech Development Policy:** Develop a domain-specific QA system that retrieves from IMF GFS reports, World Bank WDI documentation, and CAP industrial policy documents to answer questions about government spending on technology, trade balances in semiconductors, and economic complexity metrics.

---

## Group H: Infrastructure-Sustainable
**Topics:** Infra, Sustainable Finance, Resilience

*   **Available Datasets:**
    *   **OWID CO2 & UN Energy:** Detailed emission footprint data juxtaposed with macro indicators.
    *   **IMF Climate Change Indicators Dashboard:** (Planned) Directly maps to sustainable finance tracking.
    *   **Bruegel Natural Gas Imports:** High-frequency tracker showing resilience/vulnerability to energy shocks.
    *   **World Uncertainty Index (WUI) / Climate Policy Uncertainty:** To measure market reactions to sustainable policy implementations.
*   **External Sources to Target:**
    *   For sustainable finance flows, students may need to augment with **Bloomberg ESG data**, **Refinitiv ESG**, or **MSCI ESG indices**.

*   **Project Ideas:**
    *   **European Energy Resilience After the Russia Shock:** Use Bruegel Natural Gas Imports daily data (2021–present) to measure the speed and depth of import diversification away from Russia post-2022. Layer in OWID CO2 emission trends and UN Energy production-by-source to assess whether the transition accelerated renewables or substituted with other fossil fuels. GPR and WUI can proxy for geopolitical pressure driving policy urgency.
    *   **Climate Policy Uncertainty and Government Investment:** Build a cross-country panel using Climate Policy Uncertainty indices alongside IMF GFS government expenditure on infrastructure and OECD Sector Accounts gross investment data. Test whether higher climate policy uncertainty depresses or redirects public capital formation, with WDI exports-to-GDP controlling for trade exposure.
    *   **Text Classification of Infrastructure Debate Arguments:** Create a taxonomy of arguments in legislative debates around infrastructure spending (climate transition, economic stimulus, national security, jobs, fiscal sustainability). Train a multi-label classifier on CAP infrastructure-related speeches and evaluate performance across countries with different fiscal positions.
    *   **RAG System for Sustainable Infrastructure Finance:** Build a QA system that retrieves from OWID CO2 data, UN Energy reports, IMF GFS government expenditure files, and news articles to answer questions about green infrastructure spending, energy transition progress, and emission trajectories. Include source citation verification.

---

## Group I: TBD
**Topics:** AI Agents & Video Platform Behaviors (YouTube case study)

*   **Available Datasets:**
    *   This is an engineering-heavy project that falls outside of our traditional macroeconomic data pipeline.
    *   **RSS Scraper Data:** Provides a baseline of trending global news topics (BBC, NYT, Al Jazeera) to compare against trending video platform behavior.
*   **External Sources to Target:**
    *   The group will primarily rely on the **YouTube Data API (v3)** and **Google Trends API (pytrends)** to gather their core analytic dataset.

*   **Project Ideas:**
    *   **News Agenda vs. YouTube Trending Divergence:** Use the RSS Scraper live feed (BBC, NYT, Al Jazeera) to build a daily topic index, then pull YouTube trending videos via the YouTube Data API v3 for the same dates. Quantify topic overlap and lag — does YouTube trending mirror news agendas, amplify specific topics, or systematically diverge? Apply simple NLP topic classification to align the two feeds.
    *   **Search Interest and Recommendation Feedback Loops:** Use pytrends (Google Trends) to track search volume spikes for political or economic topics and compare against YouTube trending data pulled on the same day. Test whether search interest predicts YouTube trending (demand-pull) or vice versa (recommendation-push), using Granger causality or cross-correlation at the weekly level.
    *   **NLP Pipeline for Political Video Content Classification:** Build a pipeline that extracts video titles and descriptions from YouTube trending data, applies a pretrained multilingual transformer for topic classification (politics, economics, entertainment, etc.), and quantifies temporal shifts in content mix. Evaluate pipeline accuracy using a hand-labeled validation set.
    *   **Multimodal RAG for News-Video Comparison:** Build a retrieval system that takes a news headline as query and retrieves the most semantically similar YouTube video titles/descriptions from the same time period. Evaluate retrieval recall against a human-labeled alignment dataset and test whether GPT-4 generated summaries of matched pairs accurately characterize the relationship.

---

## Group J: Skilled-Immigration
**Topics:** Immigration statistics and specialized labor data

*   **Available Datasets:**
    *   **ILOSTAT:** Labor market indicators for highly skilled workers.
    *   **Comparative Agendas Project (CAP):** Laws and budgets specifically related to labor migration and visa policies.
*   **External Sources to Target:**
    *   Students should look into **IOM (International Organization for Migration)** data and specific national visa issuance statistics (e.g., H1-B data for the US).

*   **Project Ideas:**
    *   **H-1B Visa Policy and High-Skilled Labor Supply:** Combine USCIS H-1B approval/denial data with ILOSTAT employment indicators for professional occupations and CAP visa-related legislation counts. Test whether tightening visa policy reduces high-skilled labor supply in affected sectors, using difference-in-differences around key policy shifts (e.g., 2017 Buy American/Hire American order, 2020 visa suspensions).
    *   **Brain Drain Dynamics in Emerging Markets:** Use ILOSTAT annual labor data and WDI GDP per capita to build an emigration pressure index for mid-income countries. Cross-reference with OECD International Migration Database bilateral flows and IOM data to assess whether wage gaps or institutional quality (V-Dem, Freedom House) are stronger predictors of skilled emigration rates.
    *   **Skilled Immigration Speech Classifier:** Build a taxonomy of arguments used in skilled immigration debates (talent attraction, innovation, wage suppression, national preference, humanitarian) and train a classifier on CAP visa-related legislative speeches. Analyze which argument categories are most prevalent across countries and how they correlate with policy outcomes.
    *   **RAG System for Skilled Immigration Policy:** Build a retrieval-augmented QA system that answers questions about visa policies, labor market outcomes for skilled migrants, and legislative history by retrieving from CAP documents, ILOSTAT reports, and news articles. Include citation verification and factual accuracy scoring.

---

## Group R: Military-Prediction-Energy
**Topics:** (1) Energy shock and renewable energy policy adoption; (2) Military conflict prediction

*   **Available Datasets:**
    *   **UCDP/PRIO Armed Conflict Database:** Historical geolocated armed conflict events.
    *   **IMF PCPS & OpenBB:** To track global energy price shocks dynamically.
    *   **Geopolitical Risk Index (GPR) & World Uncertainty Index (WUI):** Can be used as leading indicators or features for prediction models.
    *   **CSIS North Korean Provocations / Kiel Ukraine Tracker:** Regional deep-dives on geopolitical events.

*   **Project Ideas:**
    *   **Energy Price Shocks and Renewable Policy Adoption:** Use OpenBB Commodity Futures (Crude Oil, Natural Gas) and IMF Commodities monthly price indices to identify historical energy shock episodes. Merge with OWID CO2 and UN Energy production-by-source to test whether large sustained price spikes accelerate renewable capacity additions. EPU and WUI can capture the policy uncertainty channel that may delay investment responses.
    *   **Predicting Armed Conflict Onset with Economic Indicators:** Use UCDP GED conflict event data as the outcome variable and construct a feature set from GPR (geopolitical threat vs. acts sub-indices), WUI, country-level EPU, and WDI GDP growth. Train a binary classifier (logistic regression or gradient boosting) to predict conflict onset 1–2 years ahead, evaluating out-of-sample performance and feature importance. Kiel Ukraine Tracker and CSIS data can serve as held-out regional validation sets.
    *   **NLP Pipeline for Conflict-Related Political Speeches:** Build a classifier that maps political speeches mentioning conflict or security topics onto a taxonomy of framing types (military strength, diplomatic resolution, humanitarian, economic cost, sovereignty). Use CAP legislative speeches and news articles as training data. Evaluate classifier performance and analyze temporal trends in framing across conflict episodes.
    *   **RAG System for Geopolitical Risk and Energy Policy:** Build a retrieval-augmented system that answers factual questions about energy security, conflict prediction methodology, and historical energy shocks by retrieving from UCDP GED documentation, OpenBB commodity reports, and academic sources. Include a module that flags when retrieved context contradicts GPT-generated responses.

---

## Cross-Group AI/NLP Project Ideas

These project ideas span multiple groups and focus on building reusable NLP pipelines:

*   **Political Speech Taxonomy for Immigration Policy:** Build a unified multi-label classifier that categorizes political speeches on immigration into argument taxonomies (economic opportunity, labor market impact, cultural framing, security concerns, humanitarian, fiscal burden). Train on CAP legislative speeches across multiple countries and evaluate cross-country transfer learning performance. Produce a publicly available labeled dataset.

*   **Multilingual RAG for Macroeconomic Policy Research:** Develop a cross-lingual retrieval-augmented generation system that answers policy questions by retrieving from documents in multiple languages (English, German, French, Spanish). Use embeddings from multilingual transformers (e.g., mBERT, XLM-RoBERTa) and evaluate retrieval accuracy and hallucination rates on a curated set of policy questions.

*   **Real-Time Policy Uncertainty Dashboard:** Build a pipeline that scrapes RSS feeds, classifies news articles by policy topic (immigration, trade, climate, AI) using zero-shot classification, generates daily uncertainty signals, and visualizes temporal trends with interactive charts. Integrate with existing EPU and GPR indices for validation.

(End of file - total 266 lines)
