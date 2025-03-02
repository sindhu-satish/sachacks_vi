import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

def fetch_google_cse_results(query, api_key, cse_id, max_pages=10):
    """
    Fetch search results from Google Custom Search JSON API.
    Each page returns up to 10 results.
    max_pages=10 -> up to ~100 results total (API limit).
    """
    all_results = []
    results_per_page = 10

    for page_index in range(max_pages):
        start = page_index * results_per_page + 1  # 1, 11, 21, ...
        
        url = "https://customsearch.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query,
            "start": start
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if "items" not in data:
                print(f"No more results for query '{query}' at page:", page_index + 1)
                break
            
            for item in data["items"]:
                link = item.get("link")
                title = item.get("title")
                snippet = item.get("snippet")
                
                all_results.append({
                    "url": link,
                    "title": title,
                    "snippet": snippet,
                    "query": query  # optionally, track which query returned this result
                })
        else:
            print(f"Request failed for query '{query}' with status code:", response.status_code)
            break
        
        # Optional: add a short delay to avoid hitting rate limits
        time.sleep(1)
    
    return all_results

if __name__ == "__main__":
    search_terms = [
        "career advice",
        "career guidance",
        "career path",
        "career domain",
        "career planning",
        "career exploration",
        "career discovery"
    ]
    
    combined_results = []
    
    for term in search_terms:
        query = f'site:medium.com "{term}"'
        print(f"Fetching results for query: {query}")
        results = fetch_google_cse_results(query, API_KEY, CSE_ID, max_pages=10)
        print(f"Fetched {len(results)} results for query: {term}")
        combined_results.extend(results)
    
    print(f"Total results fetched from all queries: {len(combined_results)}")
    
    # Save all the combined results to a single JSON file
    with open("results.json", "w") as json_file:
        json.dump(combined_results, json_file, indent=4)
    
    print("Results have been saved to results.json")
