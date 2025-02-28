from app.scraper import DocumentationScraper
import os
from pathlib import Path
import json

def init():
    # Create necessary directories
    docs_dir = Path("data/docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Initializing CDP documentation scraper...")
    scraper = DocumentationScraper()
    scraper.scrape_documentation()
    
    # Verify the scraped data
    verify_scraping(docs_dir)
    
def verify_scraping(docs_dir):
    """Verify that documentation was scraped and saved properly"""
    print("\nVerifying scraped documentation:")
    found_files = list(docs_dir.glob('*_docs.json'))
    
    if not found_files:
        print("Warning: No documentation files were created!")
        return
        
    total_articles = 0
    for file_path in found_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total_articles += len(data)
                print(f"\n{file_path.name}:")
                print(f"- Number of articles: {len(data)}")
                if data:
                    print(f"- First article title: {data[0]['title']}")
                    print(f"- Content preview: {data[0]['content'][:200]}...")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
    
    print(f"\nTotal articles across all CDPs: {total_articles}")

if __name__ == "__main__":
    init() 