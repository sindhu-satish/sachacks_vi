import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_medium_article(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Try to locate the main article container using <article>
            article_content = soup.find('article')
            # If <article> tag isn't found, try a div with data-field="post"
            if not article_content:
                article_content = soup.find('div', {'data-field': 'post'})
            if article_content:
                text = article_content.get_text(separator='\n')
                return text.strip()
            else:
                return None
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    input_filename = "results.json"  # Stored in the same directory
    output_filename = "scraped_articles.json"
    
    # Load JSON file containing article details
    with open(input_filename, "r") as f:
        articles = json.load(f)
    
    scraped_data = []
    
    # Iterate over each article entry
    for idx, article in enumerate(articles, start=1):
        url = article.get("url")
        if not url:
            continue
        
        print(f"Scraping article {idx}/{len(articles)}: {url}")
        content = scrape_medium_article(url)
        
        scraped_article = {
            "url": url,
            "title": article.get("title"),
            "snippet": article.get("snippet"),
            "query": article.get("query"),
            "content": content
        }
        scraped_data.append(scraped_article)
        
        # Pause briefly to avoid overwhelming the server
        time.sleep(1)
    
    # Save all scraped data into one organized JSON file
    with open(output_filename, "w") as outfile:
        json.dump(scraped_data, outfile, indent=4)
    
    print(f"Scraped articles have been saved to {output_filename}")

if __name__ == "__main__":
    main()