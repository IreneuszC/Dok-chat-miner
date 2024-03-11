map_template = """The following is a set of documents
{docs}
Based on this list of docs, please generate a concise summary.
Include key findings, arguments, and conclusions. The summary should be 3-4 sentences long and written in a clear and coherent manner.
Focus on the most important information and maintain a neutral tone throughout. 
CONCISE SUMMARY::"""


reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes. 
CONCISE SUMMARY:"""

stuff_template = """Write a concise summary of the following:
"{docs}"
CONCISE SUMMARY:"""
