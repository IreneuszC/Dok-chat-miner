# Summarizer

It uses OpenAI API to create summarization of documents and saves the results into text files.

## How to run the code?
To run the code you have to have Python 3.10.11 installed.
You have to have OpenAI Api key to use their API.

1. Add your api key to `.env.empty` file and rename it to `.env`
1. Run `pip install -r requirements.txt`
1. In [config.json](../config.json) set the path for which group method summaries should be generated <br /> 
    eg. `"scrapper/output/clustering_results/agglomerative-single/"`
1. Run `python main.py`

## How it works?

The script is reading articles dived into groups and pass each of them to OpenAI API to retrieve summary. After generating summary of each article we are combining them into one temporary summary and send it to OpenAI to retrieve the final summary for the whole group.

We are using _gpt-3.5-turbo-1106_ model to generate summaries. This model has 16,385 token limit (for simplicity token could be considered as single word, but it not always the same). This means that we cannot pass articles longer than that limit. We need also take into consideration that this limit takes into account the response from the API. 

To solve the problem of token limit we have two strategies. After file is read we check how many tokens it cost. If token number is greater than 10.000 we decide which strategy use to generate summary. 

### Strategies
1. Stuff - this strategy means that we are safe with token limit and we can pass whole article into LLM and wait for the summary of the content.
1. Map-reduce - in this approach we are dividing the article into smaller chunks. Each chunk has 10.000 characters with overlap for 500 characters. The overlap ensures that LLM has context of previous paragraph. After splitting the article into smaller paragraphs we are generating summary for each of them. After this process is finished we are combining them into one summary which is retrieved once again by gpt. This combined summary of summaries is then saved as summary of long article. Similar approach is taken for generating summary for the whole group of articles.

### Prompts
Each strategy consist of prompt combined with article content. 

* For stuff method we used simple prompt:
    ```txt
    Write a concise summary of the following:
    "{docs}"
    CONCISE SUMMARY:
    ```
* Map reduce consist of two prompts. First one generates summary for each chunk and the second one for the combined summaries:
    ```txt
    The following is a set of documents
    {docs}
    Based on this list of docs, please generate a concise summary.
    Include key findings, arguments, and conclusions. The summary should be 3-4 sentences long and written in a clear and coherent manner.
    Focus on the most important information and maintain a neutral tone throughout. 
    CONCISE SUMMARY:
    ```

    ```txt
    The following is set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary of the main themes. 
    CONCISE SUMMARY:
    ```

#### Reduced prompts

We have tried to modify the prompt to give it more context of what those article are about. We also added limit to stuff method that the summary should not be longer than 5 sentences. 

* For stuff method we used simple prompt:
    ```txt
    Write a concise summary of the following article which main topic is about security related to internet security. The summary should include key recommendations regarding protection and shortly describe vulnerabilities. Summary don't have to include information about who has been reported about vulnerabilities and where to find more information. Summary should only contain what is the problem and how to solve this. The summary should be as short as possible and not be longer than 5 sentences.
    ARTICLE:
    "{docs}"
    CONCISE SHORT SUMMARY:
    ```
* Map reduce consist of two prompts. First one generates summary for each chunk and the second one for the combined summaries:
    ```txt
    The following is a set of documents which main topic is about security related to internet security
    {docs}
    Based on this list of docs, please generate a concise summary which should include key recommendations regarding protection and shortly describe vulnerabilities. Summary don't have to include information about who has been reported about vulnerabilities and where to find more information. Summary should only contain what is the problem and how to solve this.
    The summary should be 3-4 sentences long and written in a clear and coherent manner.
    CONCISE SUMMARY:
    ```

    ```txt
    The following is set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary of the main themes. 
    CONCISE SUMMARY:
    ```

As the result summaries are a little bit shorter but not in every case. Comparison of chosen articles length in characters

| Article length | Summary | Summary reduced | Article                                                                                                                              |
| -------------- | ------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 2425           | 611     | 487             | [dbscan-eps=1;min_samples=3/government/icsa-24-011-09.txt](../scrapper/output/clustering_results/kmeans/ethernet/icsa-24-011-09.txt) |
| 2284           | 689     | 624             | [dbscan-eps=1;min_samples=3/government/icsa-24-037-02.txt](../scrapper/output/clustering_results/kmeans/ethernet/icsa-24-037-02.txt) |
| 1425           | 529     | 478             | [dbscan-eps=1;min_samples=3/government/icsa-24-023-02.txt](../scrapper/output/clustering_results/kmeans/ethernet/icsa-24-023-02.txt) |
| 77808          | 492     | 560             | [agglomerative-ward/network/icsa-24-046-11.txt](../scrapper/output/clustering_results/agglomerative-ward/network/icsa-24-046-11.txt) |
| 46967          | 574     | 596             | [agglomerative-ward/ethernet/icsa-24-046-15.txt](../scrapper/output/clustering_results/agglomerative-ward/ethernet/icsa-24-046-15.txt) |
