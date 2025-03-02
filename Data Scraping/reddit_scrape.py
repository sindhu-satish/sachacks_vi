import os
from dotenv import load_dotenv
import praw
import json
import time

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

# Initialize the Reddit instance with your credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# List of subreddits you want to scrape
subreddits = [
    "careeradvice",
    "jobs",
    "careers",
    "findapath",
    "careerguidance",
    "ApplyingToCollege"
]

all_posts = []

# Iterate over each subreddit
for subreddit_name in subreddits:
    print(f"Scraping subreddit: r/{subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    
    for submission in subreddit.new(limit=None):
        post_data = {
            "subreddit": subreddit_name,
            "id": submission.id,
            "title": submission.title,
            "url": submission.url,
            "selftext": submission.selftext,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_utc": submission.created_utc
        }
        all_posts.append(post_data)
        time.sleep(0.5)
    
    print(f"Completed scraping r/{subreddit_name}")

# Save the collected posts to a JSON file
output_filename = "reddit_subreddits_posts.json"
with open(output_filename, "w") as outfile:
    json.dump(all_posts, outfile, indent=4)

print(f"Scraping complete. Data saved to {output_filename}")