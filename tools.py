from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()


tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@tool
def web_query(query : str) -> str : 
    """Search the web for recent and reliable information on a topic. Returns titles, URLs and snippets."""
    results = tavily.search(query = query, max_results=5)

    out = []

    for r in results['results'] : 
        out.append(
            f"Title : {r['title']}\nURL : {r['url']}\nSnippet : {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)


@tool
def scrape_url(url : str) -> str :
    """Scrape and return clean text content from a given url for deeper reading"""
    try :  
        resp = requests.get(url, timeout=8, headers={"User-Agent" : "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tags in soup(["Script", "style", "nav", "footer"]): 
            tags.decompose()

        return soup.get_text(separator = " ", strip = True) [:3000]
    except Exception as e :
        return f"Could not scrape URL : {str(e)}"

print(scrape_url.invoke("https://www.cnbc.com/2026/09/08/uk-israel-sanctions-miliband-florida-trump.html"))
# print(web_query.invoke("What is the recent new of war"))