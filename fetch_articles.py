import os
import requests

API_KEY = os.environ["NEWS_API_KEY"]

URL = "https://newsapi.org/v2/everything"

SEARCH_QUERY = (
    "Poland OR Polish OR Warsaw OR "
    "\"Polish government\" OR \"Polish economy\" OR "
    "\"Poland NATO\" OR \"Poland EU\" OR \"Poland Ukraine\""
)

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

MEDIA_DOMAINS = [
    "lemonde.fr",
    "rp.pl",
    "onet.pl",
    "20min.ch",
    "nzz.ch",
    "spiegel.de",
    "bild.de",
    "wsj.com",
    "politico.com",
    "zerohedge.com",
    "insideparadeplatz.ch",
    "bbc.com"
]

ALL_DOMAINS = THINK_TANK_DOMAINS + MEDIA_DOMAINS


def categorize_source(domain):
    if domain in THINK_TANK_DOMAINS:
        return "Think Tank"
    if domain in MEDIA_DOMAINS:
        return "Media"
    return "Other"


def categorize_topic(title, description):
    text = f"{title} {description}".lower()

    if any(word in text for word in ["nato", "security", "defence", "defense", "military", "war", "army"]):
        return "Security / Military"

    if any(word in text for word in ["economy", "inflation", "market", "trade", "investment", "gdp", "growth"]):
        return "Economy"

    if any(word in text for word in ["eu", "european union", "brussels", "commission"]):
        return "Europe / EU"

    if any(word in text for word in ["election", "government", "president", "parliament", "minister", "tusk", "duda"]):
        return "Politics"

    if any(word in text for word in ["ukraine", "russia", "putin", "zelensky"]):
        return "Ukraine / Russia"

    return "General Poland"


def fetch_articles():
    all_articles = []

    for domain in ALL_DOMAINS:
        params = {
            "q": SEARCH_QUERY,
            "domains": domain,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": API_KEY
        }

        response = requests.get(URL, params=params)

        print(f"\nChecking domain: {domain}")
        print("Status:", response.status_code)

        if response.status_code != 200:
            print("Error:", response.text)
            continue

        data = response.json()

        for article in data.get("articles", []):
            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "")
            article_url = article.get("url", "")

            source_type = categorize_source(domain)
            topic = categorize_topic(title, description)

            all_articles.append({
                "domain": domain,
                "source_type": source_type,
                "topic": topic,
                "source": source,
                "title": title,
                "description": description,
                "url": article_url
            })

    return all_articles


def remove_duplicates(articles):
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article["url"]

        if url and url not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(url)

    return unique_articles


def main():
    articles = fetch_articles()
    articles = remove_duplicates(articles)

    print("\n==============================")
    print(f"FOUND {len(articles)} UNIQUE ARTICLES")
    print("==============================\n")

    for article in articles:
        print("SOURCE TYPE:", article["source_type"])
        print("DOMAIN:", article["domain"])
        print("TOPIC:", article["topic"])
        print("SOURCE:", article["source"])
        print("TITLE:", article["title"])
        print("URL:", article["url"])
        print("---")


if __name__ == "__main__":
    main()
