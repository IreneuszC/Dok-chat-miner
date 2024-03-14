# map_template = """The following is a set of documents
# {docs}
# Based on this list of docs, please generate a concise summary.
# Include key findings, arguments, and conclusions. The summary should be 3-4 sentences long and written in a clear and coherent manner.
# Focus on the most important information and maintain a neutral tone throughout.
# CONCISE SUMMARY::"""

# stuff_template = """Write a concise summary of the following:
# "{docs}"
# CONCISE SUMMARY:"""

# reduce_template = """The following is set of summaries:
# {docs}
# Take these and distill it into a final, consolidated summary of the main themes.
# CONCISE SUMMARY:"""

### Modified templates for reduced summaries:

map_template = """The following is a set of documents which main topic is about security related to internet security
{docs}
Based on this list of docs, please generate a concise summary which should include key recommendations regarding protection and shortly describe vulnerabilities. Summary don't have to include information about who has been reported about vulnerabilities and where to find more information. Summary should only contain what is the problem and how to solve this.
The summary should be 3-4 sentences long and written in a clear and coherent manner.
CONCISE SUMMARY::"""

reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes. 
CONCISE SUMMARY:"""

stuff_template = """Write a concise summary of the following article which main topic is about security related to internet security. The summary should include key recommendations regarding protection and shortly describe vulnerabilities. Summary don't have to include information about who has been reported about vulnerabilities and where to find more information. Summary should only contain what is the problem and how to solve this. The summary should be as short as possible and not be longer than 5 sentences.
ARTICLE:
"{docs}"
CONCISE SHORT SUMMARY:"""
