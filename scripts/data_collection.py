# Prep data - this makes use of the Linkedin Influencer dataset
# produced by Shreya Sajal:
# https://www.kaggle.com/datasets/shreyasajal/linkedin-influencers-data?resource=download
# %%
import re

import pandas as pd

# %%
# Load and clean data
df = pd.read_csv("../data/influencers_data.csv", low_memory=False)

# Trimming cols - the 'hashtags' column could be interesting for
# producing a specific genre of LinkedInfluencer
cols = [
    "name",
    "content",
    "media_type",
]

df = df[cols]
df = df.dropna(subset="content")
df["len"] = df["content"].apply(lambda x: len(str(x)))
# Exclude posts under 150 chars: ~20k rows
df = df[df["len"] > 150]
# %%
# Tidy up some text formatting
def clean_post(post: str) -> str:
    """
    Clean out'…see more', urls, newlines and duplicate whitespace

    eg.
    >>> post = 'Adyen  is on fire. also, the irresistible urge to acquire a
                bank license is what defines most fintech startups at one point or
                another.    #fasterpayments   #payments   #adyen   #ebay   #paypal
                \n \n \n …see more'
    >>> clean_post(test)
    'Adyen is on fire. also, the irresistible urge to acquire a bank license
    is what defines most fintech startups at one point or another. #fasterpayments
    #payments #adyen #ebay #paypal'
    """
    post = re.sub(r"…see more", "", post)
    post = re.sub(r"http\S+", "", post)
    post = re.sub(r"\n", "", post)
    post = re.sub(r" {2,}", " ", post)
    post = post.strip(" ")
    # Add post end marker
    post = f"{post}\n\n"
    return post


df["cleaned"] = df["content"].apply(clean_post)
# %%
all_content = "".join(df["cleaned"])

with open("../data/post_content.txt", "w") as f:
    f.write(all_content)
