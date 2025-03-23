# Systematic Mapping Study Data Repository

[![DOI](https://sandbox.zenodo.org/badge/953520993.svg)](https://handle.stage.datacite.org/10.5072/zenodo.187824)

This repository contains the data and analysis scripts for a systematic mapping study. The repository includes raw data from literature databases, processed datasets, and analysis notebooks.

## Repository Contents

### Raw Data Files
- `75_scopus_full.csv`: Raw data extracted from Scopus database (excluding 2024 data)
- `445_wos.csv`: Raw data extracted from Web of Science database (excluding 2024 data)

### Processed Data Files
- `database.csv`: Final consolidated database used for generating charts and analysis in the systematic mapping study
- `pdf_full_texts.csv`: Contains the full text content of papers used for generating the word cloud analysis

### Analysis Notebooks
- `charts-scripts.ipynb`: Jupyter notebook containing scripts for data analysis and chart generation
- `wordcloud.ipynb`: Jupyter notebook dedicated to word cloud generation and text analysis

## Data Timeline
Please note that the raw data files (`75_scopus_full.csv` and `445_wos.csv`) do not include publications from 2024. The analysis is based on data up to 2023.

## Analysis Workflow
1. Raw data was collected from Scopus (75 entries) and Web of Science (445 entries)
2. Data was processed and consolidated into `database.csv` for analysis
3. Full-text content was extracted and stored in `pdf_full_texts.csv` for text analysis
4. Analysis was performed using two separate notebooks:
   - Main analysis and visualizations in `charts-scripts.ipynb`
   - Text analysis and word cloud generation in `wordcloud.ipynb` 