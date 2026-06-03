import os
import json
import requests
from datetime import datetime, timezone

API_KEY = os.environ["NEWS_API_KEY"]

NEWS_DOMAINS = [
    # Western / Polish / Swiss / German / European media
    "lemonde.fr",
    "dorzeczy.pl",
    "onet.pl",
    "20min.ch",
    "nzz.ch",
    "spiegel.de",
    "bild.de",
    "wsj.com",
    "politico.eu",
    "zerohedge.com",
    "insideparadeplatz.ch",
    "bbc.com",

    # Russian media
    "themoscowtimes.com",
    "kommersant.ru",
    "rbc.ru",
    "vedomosti.ru",
    "novayagazeta.eu",

    # Belarusian media
    "zerkalo.io",
    "charter97.org",
    "belsat.eu",
    "euroradio.fm",
    "reform.news",

    # Ukrainian media
    "kyivindependent.com",
    "pravda.com.ua",
    "zn.ua",
    "nv.ua",
    "liga.net",

    # Chinese / Hong Kong media
    "chinadaily.com.cn",
    "globaltimes.cn",
    "english.news.cn",
    "en.people.cn",
    "scmp.com",

    # Japanese media
    "japantimes.co.jp",
    "asia.nikkei.com",
    "asahi.com",
    "mainichi.jp",
    "yomiuri.co.jp",

    # Singaporean media
    "channelnewsasia.com",
    "straitstimes.com",
    "businesstimes.com.sg"
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

POLAND_TERMS = [
    "Poland",
    "Polish",
    "Warsaw",
    "Warszawa",
    "Polska",
    "Polski",
    "Polish government",
    "Polish economy",
    "Polish security",
    "Polish military",
    "Poland NATO",
    "Poland EU",
    "Poland Ukraine",

    # Russian
    "Польша",
    "Польши",
    "Польшу",
    "польский",
    "польская",
    "Варшава",

    # Ukrainian
    "Польща",
    "Польщі",
    "Польщу",
    "польський",
    "польська",
    "Варшава"
]

POLITICIANS = [
    "Donald Tusk",
    "Karol Nawrocki",
    "Radoslaw Sikorski",
    "Radosław Sikorski",
    "Krzysztof Bosak",
    "Andrzej Duda",
    "Jaroslaw Kaczynski",
    "Jarosław Kaczyński",
    "Mateusz Morawiecki",
    "Szymon Holownia",
    "Szymon Hołownia",
    "Rafal Trzaskowski",
    "Rafał Trzaskowski",
    "Grzegorz Braun",
    "Slawomir Mentzen",
    "Sławomir Mentzen",
    "Wladyslaw Kosiniak-Kamysz",
    "Władysław Kosiniak-Kamysz",
    "Robert Biedron",
    "Robert Biedroń",
    "Adrian Zandberg",
    "Beata Szydlo",
    "Beata Szydło",
    "Mariusz Blaszczak",
    "Mariusz Błaszczak",
    "Antoni Macierewicz",
    "Zbigniew Ziobro",
    "Patryk Jaki",
    "Przemyslaw Czarnek",
    "Przemysław Czarnek",
    "Borys Budka",
    "Tomasz Siemoniak",
    "Adam Bodnar",
    "Marcin Kierwinski",
    "Marcin Kierwiński",
    "Katarzyna Pelczynska-Nalecz",
    "Katarzyna Pełczyńska-Nałęcz",
    "Agnieszka Dziemianowicz-Bak",
    "Barbara Nowacka",
    "Izabela Leszczyna",
    "Dariusz Wieczorek",
    "Krzysztof Gawkowski",
    "Waldemar Buda",
    "Jacek Sasin",
    "Elzbieta Witek",
    "Elżbieta Witek",
    "Malgorzata Kidawa-Blonska",
    "Małgorzata Kidawa-Błońska",
    "Roman Giertych",
    "Michal Kolodziejczak",
    "Michał Kołodziejczak",
    "Mariusz Kaminski",
    "Mariusz Kamiński",
    "Maciej Wasik",
    "Maciej Wąsik",
    "Piotr Glinski",
    "Piotr Gliński"
]

KEYWORDS = POLAND_TERMS + POLITICIANS

SOURCE_IMPORTANCE = {
    # Western / Polish / Swiss / German / European media
    "bbc.com": 10,
    "wsj.com": 10,
    "politico.eu": 9,
    "lemonde.fr": 9,
    "spiegel.de": 9,
    "nzz.ch": 8,
    "onet.pl": 7,
    "dorzeczy.pl": 6,
    "20min.ch": 5,
    "bild.de": 6,
    "insideparadeplatz.ch": 5,
    "zerohedge.com": 5,

    # Think tanks
    "csis.org": 10,
    "rand.org": 10,
    "atlanticcouncil.org": 9,
    "brookings.edu": 9,
    "carnegieendowment.org": 9,
    "cnas.org": 9,
    "cepa.org": 8,
    "heritage.org": 8,
    "wilsoncenter.org": 8,

    # Russian media
    "themoscowtimes.com": 8,
    "kommersant.ru": 7,
    "rbc.ru": 7,
    "vedomosti.ru": 7,
    "novayagazeta.eu": 8,

    # Belarusian media
    "zerkalo.io": 7,
    "charter97.org": 7,
    "belsat.eu": 8,
    "euroradio.fm": 6,
    "reform.news": 6,

    # Ukrainian media
    "kyivindependent.com": 9,
    "pravda.com.ua": 8,
    "zn.ua": 7,
    "nv.ua": 7,
    "liga.net": 7,

    # Chinese / Hong Kong media
    "chinadaily.com.cn": 7,
    "globaltimes.cn": 7,
    "english.news.cn": 8,
    "en.people.cn": 7,
    "scmp.com": 8,

    # Japanese media
    "japantimes.co.jp": 8,
    "asia.nikkei.com": 9,
    "asahi.com": 8,
    "mainichi.jp": 7,
    "yomiuri.co.jp": 8,

    # Singaporean media
    "channelnewsasia.com": 8,
    "straitstimes.com": 8,
    "businesstimes.com.sg": 7
}


def article_text(article):
    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""
    return f"{title} {description} {content}".lower()


def is_really_about_poland(article):
    text = article_text(article)

    direct_poland_terms = [
        "poland",
        "polish",
        "warsaw",
        "polska",
        "polski",
        "polacy",
        "poland's",
        "polish government",
        "polish economy",
        "polish military",

        # Russian
        "польша",
        "польши",
        "польшу",
        "польский",
        "польская",
        "варшава",

        # Ukrainian
        "польща",
        "польщі",
        "польщу",
        "польський",
        "польська",
        "варшава"
    ]

    if any(term in text for term in direct_poland_terms):
        return True

    for name in POLITICIANS:
        if name.lower() in text:
            return True

    return False


def detect_people(article):
    text = article_text(article)
    found_people = []

    for person in POLITICIANS:
        if person.lower() in text:
            found_people.append(person)

    return sorted(list(set(found_people)))


def categorize_article(title, description):
    text = f"{title} {description}".lower()

    if any(word in text for word in [
        "nato",
        "military",
        "defence",
        "defense",
        "security",
        "war",
        "army",
        "border",
        "missile",
        "troops",
        "defence spending",
        "defense spending",
        "cyber",
        "hybrid war"
    ]):
        return "Security"

    if any(word in text for word in [
        "economy",
        "inflation",
        "market",
        "trade",
        "gdp",
        "investment",
        "energy",
        "gas",
        "oil",
        "budget",
        "deficit",
        "interest rates",
        "zloty",
        "currency",
        "exports",
        "imports"
    ]):
        return "Economy"

    if any(word in text for word in [
        "eu",
        "european union",
        "brussels",
        "commission",
        "european parliament",
        "rule of law",
        "european court"
    ]):
        return "Europe / EU"

    if any(word in text for word in [
        "government",
        "election",
        "president",
        "minister",
        "parliament",
        "party",
        "coalition",
        "opposition",
        "prime minister",
        "cabinet"
    ]):
        return "Politics"

    if any(word in text for word in [
        "ukraine",
        "russia",
        "russian",
        "putin",
        "zelensky",
        "kyiv",
        "moscow",
        "belarus",
        "lukashenko",
        "kremlin"
    ]):
        return "Ukraine / Russia / Belarus"

    if any(word in text for word in [
        "migration",
        "migrant",
        "refugee",
        "border crisis",
        "asylum"
    ]):
        return "Migration"

    if any(word in text for word in [
        "china",
        "chinese",
        "beijing",
        "japan",
        "tokyo",
        "singapore",
        "asia",
        "indo-pacific"
    ]):
        return "Asia / Indo-Pacific"

    return "General Poland"


def calculate_importance(article, domain, keyword, category):
    score = 0

    score += SOURCE_IMPORTANCE.get(domain, 3)

    important_keywords = [
        "Poland NATO",
        "Poland Ukraine",
        "Polish security",
        "Polish military",
        "Polish government",
        "Donald Tusk",
        "Radoslaw Sikorski",
        "Radosław Sikorski",
        "Karol Nawrocki",
        "Krzysztof Bosak",
        "Andrzej Duda",
        "Jaroslaw Kaczynski",
        "Jarosław Kaczyński",
        "Mateusz Morawiecki",
        "Rafal Trzaskowski",
        "Rafał Trzaskowski"
    ]

    if keyword in important_keywords:
        score += 5
    else:
        score += 2

    if category in ["Security", "Politics", "Ukraine / Russia / Belarus"]:
        score += 5
    elif category in ["Economy", "Europe / EU", "Asia / Indo-Pacific"]:
        score += 4
    elif category == "Migration":
        score += 4
    else:
        score += 2

    published_at = article.get("publishedAt")

    if published_at:
        try:
            published_date = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            hours_old = (now - published_date).total_seconds() / 3600

            if hours_old <= 24:
                score += 5
            elif hours_old <= 72:
                score += 3
            elif hours_old <= 168:
                score += 2
            else:
                score += 1
        except Exception:
            pass

    people_found = detect_people(article)
    score += min(len(people_found) * 2, 6)

    return score


def importance_label(score):
    if score >= 25:
        return "Very High"
    if score >= 18:
        return "High"
    if score >= 12:
        return "Medium"
    return "Low"


def build_query(keyword):
    return f'"{keyword}" AND (Poland OR Polish OR Warsaw OR Polska OR Польша OR Польща)'


def search_articles(domains, source_type):
    url = "https://newsapi.org/v2/everything"
    results = []

    for domain in domains:
        for keyword in KEYWORDS:
            query = build_query(keyword)

            params = {
                "q": query,
                "domains": domain,
                "sortBy": "publishedAt",
                "pageSize": 10,
                "apiKey": API_KEY
            }

            response = requests.get(url, params=params)

            print(f"Searching {source_type}: {domain} | keyword: {keyword}")
            print("Status:", response.status_code)

            if response.status_code == 426:
                print("NewsAPI plan limit or endpoint restriction.")
                continue

            if response.status_code == 429:
                print("Daily request limit reached.")
                return results

            if response.status_code != 200:
                print("Error:", response.text)
                continue

            data = response.json()

            for article in data.get("articles", []):
                if not is_really_about_poland(article):
                    continue

                title = article.get("title") or ""
                description = article.get("description") or ""
                article_url = article.get("url") or ""

                if not article_url:
                    continue

                category = categorize_article(title, description)
                score = calculate_importance(article, domain, keyword, category)
                people = detect_people(article)

                results.append({
                    "fetched_at": datetime.utcnow().isoformat(),
                    "published_at": article.get("publishedAt"),
                    "source_type": source_type,
                    "source_domain": domain,
                    "source": article.get("source", {}).get("name"),
                    "title": title,
                    "description": description,
                    "url": article_url,
                    "keyword": keyword,
                    "category": category,
                    "people": people,
                    "importance_score": score,
                    "importance_label": importance_label(score)
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


def load_existing_articles():
    try:
        with open("data/articles.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_articles(articles):
    os.makedirs("data", exist_ok=True)

    with open("data/articles.json", "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=2)


def main():
    print("Starting Poland media monitor...")

    old_articles = load_existing_articles()
    new_articles = []

    new_articles.extend(search_articles(NEWS_DOMAINS, "Newspaper"))
    new_articles.extend(search_articles(THINK_TANK_DOMAINS, "Think Tank"))

    all_articles = old_articles + new_articles
    all_articles = remove_duplicates(all_articles)

    all_articles = sorted(
        all_articles,
        key=lambda x: x.get("importance_score", 0),
        reverse=True
    )

    print(f"Found {len(new_articles)} new raw articles.")
    print(f"Saved {len(all_articles)} total unique articles.")

    save_articles(all_articles)

    print("Saved articles to data/articles.json")
    print("Finished.")


if __name__ == "__main__":
    main()
