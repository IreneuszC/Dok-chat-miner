import os
from rewarder import Rewarder
rewarder = Rewarder(os.path.join('trained_models','sample.model'))
article = 'This is an example article. Article includes more information than the summary.'
summary = 'This is an example summary.'
score = rewarder(article,summary)
print(f"\nArticle: {article}")
print(f"Summary: {summary}")
print(f"Score: {score}")

doc = 'An information campaign urging the public to "get ready for Brexit" has been launched by the government. ' \
    'The campaign began on Sunday with the launch of a website, gov.uk/brexit.' \
    'Billboards and social media adverts will appear in the coming days and TV adverts will air later this month.' \
    'Michael Gove, who is in charge of no-deal plans, said the adverts encourage "shared responsibility" for preparing to leave the EU on 31 October.' \
    'It has been reported that the campaign could cost as much as £100m as ministers seek to inform people what they might need to do, if anything, ahead of the deadline.'
summ1 = 'Get ready for Brexit advertising campaign launches'

score = rewarder(doc,summary)
print(f"\nArticle: {doc}")
print(f"Summary: {summary}")
print(f"Score: {score}")

doc = 'An information campaign urging the public to "get ready for Brexit" has been launched by the government. ' \
    'The campaign began on Sunday with the launch of a website, gov.uk/brexit.' \
    'Billboards and social media adverts will appear in the coming days and TV adverts will air later this month.' \
    'Michael Gove, who is in charge of no-deal plans, said the adverts encourage "shared responsibility" for preparing to leave the EU on 31 October.' \
    'It has been reported that the campaign could cost as much as £100m as ministers seek to inform people what they might need to do, if anything, ahead of the deadline.'
summ1 = 'Get ready for Brexit advertising campaign launches'

score = rewarder(doc, doc)
print(f"\nArticle: {doc}")
print(f"Summary: {doc}")
print(f"Score: {score}")

doc = 'An information campaign urging the public to "get ready for Brexit" has been launched by the government. ' \
    'The campaign began on Sunday with the launch of a website, gov.uk/brexit.' \
    'Billboards and social media adverts will appear in the coming days and TV adverts will air later this month.' \
    'Michael Gove, who is in charge of no-deal plans, said the adverts encourage "shared responsibility" for preparing to leave the EU on 31 October.' \
    'It has been reported that the campaign could cost as much as £100m as ministers seek to inform people what they might need to do, if anything, ahead of the deadline.'
summ1 = "Nothing!"

score = rewarder(doc, summ1)
print(f"\nArticle: {doc}")
print(f"Summary: {summ1}")
print(f"Score: {score}")

article = 'This is an example article. Article includes more information than the summary.'
summary = 'This is an example summary.'
score = rewarder(article,summary)
print(f"\nArticle: {article}")
print(f"Summary: {summary}")
print(f"Score: {score}")