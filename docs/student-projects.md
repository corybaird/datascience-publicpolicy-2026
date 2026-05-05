# Student Project Ideas and Dataset Mappings

This document maps student project ideas to existing or planned datasets within our macroeconomic data repository, and suggests external data sources where our coverage might currently be limited. 

## Group A & J: Immigration
**Topics:** Immigration related / Immigration statistics and text data

*   **Available Datasets:**
    *   **ILOSTAT (Monthly/Annual):** Extensive labor market indicators which often encompass demographics and labor force structures. 
    *   **UN SDG & Demographic Data:** Broad population and sustainable development variables.
*   **External Sources to Target:**
    *   Our internal database is structurally light on direct bilateral migration flows. Students should look into the **UN DESA International Migrant Stock** database or **OECD International Migration Database**. If text data is needed, parsing immigration-related political speeches or scraping news media for sentiment analysis (similar to the SF Fed News Sentiment logic) could be a strong approach.

## Group B: AI Policy and Economic Freedom
**Topics:** AI Policy and Economic Freedom

*   **Available Datasets:**
    *   **Heritage Economic Freedom Index (EFI):** Annual coverage of economic freedom scores globally.
    *   **Freedom House & V-Dem / Polity5:** Deep institutional quality and civil liberties metrics. 
    *   **Economic Freedom of the World (Cato/Fraser):** (Planned) For broader institutional coverage.
*   **External Sources to Target:**
    *   Currently, we don't have dedicated datasets mapping AI policy adoption. Students should cross-reference our economic freedom datasets with the **Stanford AI Index Report**, **Oxford Insights Government AI Readiness Index**, or OECD AI policy observatories.

## Group C: Media and Politics
**Topics:** Media and politics

*   **Available Datasets:**
    *   **SF Fed Daily News Sentiment Index:** High-frequency news sentiment analysis for the US. 
    *   **Geopolitical Risk Index (GPR):** Daily/Monthly news-based text mining of geopolitical risk factors globally.
    *   **Economic Policy Uncertainty (EPU):** News-based text index tracking policy uncertainty across 25+ countries.
    *   **V-Dem (Varieties of Democracy):** Has specialized modules evaluating media freedom, censorship, and political pluralism.

## Group D: Tariff Pass-through
**Topics:** Pass-through of 2025 Trump tariffs to US consumer prices (comparing inflation index categories for tariff-exposed vs. non-exposed goods)

*   **Available Datasets:**
    *   **FRED / Cleveland Fed:** Disaggregated US CPI and PCE indicators.
    *   **NY Fed Global Supply Chain Pressure Index (GSCPI):** Proxy for supply chain disruption effects.
    *   **IMF Commodities & OpenBB Commodity Futures:** To track raw material costs prior to manufacturing. 
    *   **Kiel Trade Indicator:** (Planned) Monthly trade flow estimates which highlight immediate shocks to imports.
*   **External Sources to Target:**
    *   Students will need to acquire highly disaggregated tariff schedules (e.g., from the **USTR** or the **PIIE Trump Tariff Tracker**) and merge these timelines with our disaggregated FRED CPI data (by specific durable and non-durable goods categories).

## Group G: International Orgs, Tech, Developmental, & Social Policy
**Topics:** International Organizations Data, Tech industry development & semiconductors, Developmental states, Social policy (cash transfers) & culture

*   **Available Datasets:**
    *   **World Bank WDI / IMF (BOP, GFS, etc.) / OECD QNA:** Deep historical tracking of government spending and economic structural balances. 
    *   **SWIID (Standardized World Income Inequality Database):** Ideal for social policy; tracks both market income (pre-tax/transfer) and disposable income, demonstrating the efficacy of redistribution (cash transfers).
    *   **UN SDG / UNCTADstat:** Coverage of socio-economic and development metrics.
    *   **Bruegel European Clean Tech Tracker:** (Planned) Useful for tracking early iterations of high-tech manufacturing policies.
*   **External Sources to Target:**
    *   For semiconductors, specific data from the **Semiconductor Industry Association (SIA)** or tech-specific trade volume APIs might be necessary to augment the UN Comtrade data we have.

## Group H: Infrastructure, Sustainable Finance, Resilience
**Topics:** Infra, Sustainable Finance, Resilience

*   **Available Datasets:**
    *   **OWID CO2 & UN Energy:** Detailed emission footprint data juxtaposed with macro indicators.
    *   **IMF Climate Change Indicators Dashboard:** (Planned) Directly maps to sustainable finance tracking.
    *   **Bruegel Natural Gas Imports:** High-frequency tracker showing resilience/vulnerability to energy shocks. 
    *   **World Uncertainty Index (WUI) / Climate Policy Uncertainty:** To measure market reactions to sustainable policy implementations.

## Group I: AI Agents & Video Platform Behaviors
**Topics:** Using AI agents to analyze user search behavior and trending topics on video platforms, using YouTube as a case study. 

*   **Available Datasets:**
    *   This is an engineering-heavy project that falls outside of our traditional macroeconomic data pipeline. However, the logic applied in our existing API scraping scripts (like OpenBB or SF Fed) can be directly adapted.
*   **External Sources to Target:**
    *   The group will primarily rely on the **YouTube Data API (v3)** and **Google Trends API (pytrends)** to gather their core analytic dataset. 

## Group R: Energy Shocks & Armed Conflict
**Topics:** 
(1) Energy shock and renewable energy policy adoption 
(2) Military conflict simulation and prediction

*   **Available Datasets for Project 1:**
    *   **IMF Primary Commodity Price System (PCPS) & OpenBB Commodity Futures:** To track global energy price shocks dynamically. 
    *   **UN Energy & OWID CO2:** Can trace output changes or transition speeds post-energy shock. 
*   **Available Datasets for Project 2:**
    *   **UCDP GED & UCDP/PRIO Armed Conflict Database:** The gold standard for historical geolocated armed conflict events. 
    *   **Geopolitical Risk Index (GPR) & World Uncertainty Index (WUI):** Can be used as leading indicators or features for prediction models.
    *   **CSIS North Korean Provocations / Kiel Ukraine Tracker:** Regional deep-dives on geopolitical events.
