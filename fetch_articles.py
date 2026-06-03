import os
import json
import requests
from datetime import datetime

API_KEY = os.environ["NEWS_API_KEY"]

NEWS_DOMAINS = [
    "lemonde.fr",
    "dorzeczy.pl",
    "onet.pl",
    "20min.ch",
    "nzz.ch",
    "spiegel.de",
    "bild.de",
    "wsj.com",
    "politico.eu",
    "zero.pl",
    "insideparadeplatz.ch",
    "bbc.com"
]

THINK_TANK_DOMAINS = [
    "csis.org",
    "atlanticcouncil.org",
    "rand.org",
    "cepa.org",
    "heritage.org",
    "carnegieendowment.org",
    "brookings.edu",
    "wilsoncenter.org",
    "cnas.org"
]

KEYWORDS = [
    "Poland",
    "Polish",
    "Warsaw",
    "Poland NATO",
    "Poland EU",
    "Poland Ukraine",
    "Polish economy",
    "Polish government",
    "Polish security",
    "Polish military"
]


def categorize_article(title, description):
    text = f"{title} {description}".lower()

    if any(word in text for word in ["nato", "military", "defence", "defense", "security", "war", "army"]):
        return "Security"

    if any(word in text for word in ["economy", "inflation", "market", "trade", "gdp", "investment"]):
        return "Economy"

    if any(word in text for word in ["eu", "european union", "brussels"]):
        return "Europe / EU"

    if any(word in text for word in ["government", "election", "president", "minister", "parliament"]):
        return "Politics"

    return "General"


def search_articles(domains, source_type):
    url = "https://newsapi.org/v2/everything"
    domain_string = ",".join(domains)

    results = []

    for keyword in KEYWORDS:
        params = {
            "q": keyword,
            "domains": domain_string,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        print(f"Searching {source_type} for keyword: {keyword}")
        print("Status:", response.status_code)

        if response.status_code != 200:
            continue

        data = response.json()

        for article in data.get("articles", []):
            title = article.get("title") or ""
            description = article.get("description") or ""
            article_url = article.get("url") or ""

            results.append({
                "fetched_at": datetime.utcnow().isoformat(),
                "published_at": article.get("publishedAt"),
                "source_type": source_type,
                "source": article.get("source", {}).get("name"),
                "title": title,
                "description": description,
                "url": article_url,
                "keyword": keyword,
                "category": categorize_article(title, description)
            })

    return results


def remove_duplicates(articles):
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get("url")

        if url and url not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(url)

    return unique_articles


def main():
    print("Starting Poland media monitor...")

    all_articles = []

    all_articles.extend(search_articles(NEWS_DOMAINS, "Newspaper"))
    all_articles.extend(search_articles(THINK_TANK_DOMAINS, "Think Tank"))

    all_articles = remove_duplicates(all_articles)

    print(f"Found {len(all_articles)} unique articles.")

    import os
    os.makedirs("data", exist_ok=True)

    with open("data/articles.json", "w", encoding="utf-8") as file:
        json.dump(all_articles, file, ensure_ascii=False, indent=2)

    print("Saved articles to data/articles.json")
    print("Finished.")


if __name__ == "__main__":
    main()
