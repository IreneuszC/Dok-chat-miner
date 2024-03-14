## Scrapper

Scrapper that fetches cybersecurity articles located on ``cisa.gov`` website.
It processes text cleansing and groups articles using several grouping methods like: k-means, agglomerate and DBSCAN and assigns most suitability group to given query terms.

Example output after grouping:
```
Kmeans clusters: 3
method: kmeans
labels [2 1 1 2 0 1 1 1 2 2 2 1 2 2 2 0 0 1 1 1 1 1 0 2 2 2 0 2 1 1 1 1 1 2 1 2 2
 2 1 1 1 2 2 2 1 0 1 0 2 2 1 0]
silhouette_score: 0.02582353266239743
output/clustering_results silhouette kmeans,3,0.02582353266239743

Top terms per cluster:
Cluster 0:
 electric
 mitsubishi
 vulnerability
 cisa
 aveva
 disclose
 information
 modules
 products
 tamper

Cluster 1:
 siemens
 cisa
 vulnerability
 cvss
 security
 score
 information
 recommends
 assigned
 following

Cluster 2:
 cvss
 vulnerability
 assigned
 cisa
 score
 string
 base
 vector
 v3
 calculated


Prediction:
ethernet:[2]
government:[2]
network:[2]
```
Scrapper groups articles by most suitable cluster related to query term.

Example ``output/clustering_results`` structure after grouping articles:

![clustering_results_structure.png](screenshots%2Fclustering_results_structure.png)

## How to run
1. If you're using Anaconda, build new environment:
```
conda env create -f environment.yml
```
2. If you're not using Anaconda, install all needed packages (make sure you are using 3.8.10 Python version):
```
pip install -r requirements.txt
```
3. Check ifs to run specific actions in ``main.py``:
* 1-st if - run scrapper and save articles to one file
* 2-st if - run text cleaner
* 5-7 ifs - run specific clustering method (kmeans, dbscan, agglomerate)
3. To run scraper and cluster articles run ``main.py`` file.
4. Scraped articles and clustered in groups related to ``query terms`` were saved in ``output/clustering_results``.

## Configuration

Configuration file: ``configurator.py``

1. How much pages that contains links to articles to scrap (from first page):
```python
PAGES_TO_SCRAP = 5
```

2. Number of clusters:
```python
CLUSTERS_NUMBER = 3
```

3. Query terms (final groups):
```python
QUERY_TERMS = ['ethernet', 'government', 'network']
```