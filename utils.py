import re
import requests
from bs4 import BeautifulSoup

def clean_text(text):
    # Clean up text input
    text = re.sub(r'<[^>]*?>', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_google_scholar_data(profile_url):
    # Fetch professor's details from a direct Google Scholar profile URL
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        response = requests.get(profile_url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to fetch profile. HTTP status code: {response.status_code}"}
        
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract name
        name = soup.find("div", {"id": "gsc_prf_in"}).text.strip()

        # Extract research interests
        interests = [i.text.strip() for i in soup.find_all("a", {"class": "gsc_prf_inta"})]

        # Extract recent publications
        publications = []
        for pub in soup.find_all("tr", {"class": "gsc_a_tr"})[:5]:
            title = pub.find("a", {"class": "gsc_a_at"}).text.strip()
            publications.append(title)

        return {
            "name": name,
            "interests": interests,
            "recent_papers": publications,
        }
    except Exception as e:
        return {"error": str(e)}
