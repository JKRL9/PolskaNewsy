import os
import json
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse

API_KEY = os.environ["NEWS_API_KEY"]

MEDIA_GROUPS = {
    "Polish media": [
        "dorzeczy.pl",
        "onet.pl"
    ],

    "European / Western media": [
        "lemonde.fr",
        "20min.ch",
        "nzz.ch",
        "spiegel.de",
        "bild.de",
        "wsj.com",
        "politico.eu",
        "zerohedge.com",
        "insideparadeplatz.ch",
        "bbc.com"
    ],

    "Foreign policy / strategy magazines": [
        "foreignaffairs.com",
        "foreignpolicy.com",
        "thediplomat.com",
        "nationalinterest.org",
        "warontherocks.com",
        "worldpoliticsreview.com",
        "geopoliticalmonitor.com",
        "responsiblestatecraft.org",
        "lawfaremedia.org",
        "mondediplo.com"
    ],

    "Russian / Belarusian media": [
        "themoscowtimes.com",
        "kommersant.ru",
        "rbc.ru",
        "vedomosti.ru",
        "novayagazeta.eu",
        "zerkalo.io",
        "charter97.org",
        "belsat.eu",
        "euroradio.fm",
        "reform.news"
    ],

    "Ukrainian media": [
        "kyivindependent.com",
        "pravda.com.ua",
        "zn.ua",
        "nv.ua",
        "liga.net"
    ],

    "Asian media": [
        "chinadaily.com.cn",
        "globaltimes.cn",
        "english.news.cn",
        "en.people.cn",
        "scmp.com",
        "japantimes.co.jp",
        "asia.nikkei.com",
        "asahi.com",
        "mainichi.jp",
        "yomiuri.co.jp",
        "channelnewsasia.com",
        "straitstimes.com",
        "businesstimes.com.sg"
    ],

    "Think tanks": [
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
}

POLAND_TERMS = [
    # English
    "Poland",
    "Polish",
    "Warsaw",
    "Polish government",
    "Polish economy",
    "Polish security",
    "Polish military",
    "Poland NATO",
    "Poland EU",
    "Poland Ukraine",

    # Polish
    "Polska",
    "Polski",
    "Polskę",
    "Polsce",
    "Polaków",
    "Warszawa",
    "rząd Polski",
    "polska gospodarka",
    "polskie wojsko",
    "polskie bezpieczeństwo",

    # German
    "Polen",
    "polnisch",
    "polnische",
    "polnischer",
    "Warschau",
    "polnische Regierung",
    "polnische Wirtschaft",
    "polnisches Militär",

    # French
    "Pologne",
    "polonais",
    "polonaise",
    "Varsovie",
    "gouvernement polonais",
    "économie polonaise",

    # Spanish
    "Polonia",
    "polaco",
    "polaca",
    "Varsovia",
    "gobierno polaco",

    # Italian
    "Polonia",
    "polacco",
    "polacca",
    "Varsavia",
    "governo polacco",

    # Russian
    "Польша",
    "Польши",
    "Польшу",
    "Польше",
    "польский",
    "польская",
    "польское",
    "Варшава",
    "польское правительство",
    "польская экономика",
    "польская армия",

    # Belarusian
    "Польшча",
    "Польшчы",
    "Польшчу",
    "польскі",
    "польская",
    "Варшава",

    # Ukrainian
    "Польща",
    "Польщі",
    "Польщу",
    "польський",
    "польська",
    "польське",
    "Варшава",
    "польський уряд",
    "польська економіка",
    "польська армія",

    # Chinese simplified / traditional
    "波兰",
    "波蘭",
    "华沙",
    "華沙",
    "波兰政府",
    "波蘭政府",
    "波兰经济",
    "波蘭經濟",
    "波兰军队",
    "波蘭軍隊",

    # Japanese
    "ポーランド",
    "ポランド",
    "ワルシャワ",
    "ポーランド政府",
    "ポーランド経済",
    "ポーランド軍",

    # Korean
    "폴란드",
    "바르샤바",
    "폴란드 정부",
    "폴란드 경제",
    "폴란드 군대",

    # Portuguese
    "Polônia",
    "Polonia",
    "polonês",
    "polonesa",
    "Varsóvia",

    # Dutch
    "Polen",
    "Pools",
    "Poolse",
    "Warschau",

    # Swedish / Norwegian / Danish
    "Polen",
    "polsk",
    "polska",
    "Warszawa",

    # Czech / Slovak
    "Polsko",
    "polský",
    "polská",
    "Varšava",

    # Hungarian
    "Lengyelország",
    "lengyel",
    "Varsó"
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

SOURCE_IMPORTANCE = {
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

    "foreignaffairs.com": 10,
    "foreignpolicy.com": 10,
    "thediplomat.com": 8,
    "nationalinterest.org": 8,
    "warontherocks.com": 9,
    "worldpoliticsreview.com": 8,
    "geopoliticalmonitor.com": 7,
    "responsiblestatecraft.org": 7,
    "lawfaremedia.org": 8,
    "mondediplo.com": 8,

    "csis.org": 10,
    "rand.org": 10,
    "atlanticcouncil.org": 9,
    "brookings.edu": 9,
    "carnegieendowment.org": 9,
    "cnas.org": 9,
    "cepa.org": 8,
    "heritage.org": 8,
    "wilsoncenter.org": 8,

    "themoscowtimes.com": 8,
    "kommersant.ru": 7,
    "rbc.ru": 7,
    "vedomosti.ru": 7,
    "novayagazeta.eu": 8,

    "zerkalo.io": 7,
    "charter97.org": 7,
    "belsat.eu": 8,
    "euroradio.fm": 6,
    "reform.news": 6,

    "kyivindependent.com": 9,
    "pravda.com.ua": 8,
    "zn.ua": 7,
    "nv.ua": 7,
    "liga.net": 7,

    "chinadaily.com.cn": 7,
    "globaltimes.cn": 7,
    "english.news.cn": 8,
    "en.people.cn": 7,
    "scmp.com": 8,

    "japantimes.co.jp": 8,
    "asia.nikkei.com": 9,
    "asahi.com": 8,
    "mainichi.jp": 7,
    "yomiuri.co.jp": 8,

    "channelnewsasia.com": 8,
    "straitstimes.com": 8,
    "businesstimes.com.sg": 7
}


def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "").lower()
    except Exception:
        return ""


def article_text(article):
    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""
    return f"{title} {description} {content}".lower()


def is_really_about_poland(article):
    text = article_text(article)

    for term in POLAND_TERMS:
        if term.lower() in text:
            return True

    for person in POLITICIANS:
        if person.lower() in text:
            return True

    return False


def detect_people(article):
    text = article_text(article)
    found_people = []

    for person in POLITICIANS:
        if person.lower() in text:
            found_people.append(person)

    return sorted(list(set(found_people)))


def detect_media_group(domain):
    for group_name, domains in MEDIA_GROUPS.items():
        if domain in domains:
            return group_name

    return "Other"


def categorize_article(title, description):
    text = f"{title} {description}".lower()

    if any(word in text for word in [
        "nato", "military", "defence", "defense", "security", "war",
        "army", "border", "missile", "troops", "cyber", "hybrid war",
        "deterrence", "eastern flank", "wojsko", "bezpieczeństwo",
        "война", "армия", "безопасность", "війна", "армія", "безпека",
        "軍", "安全保障", "军事", "安全"
    ]):
        return "Security"

    if any(word in text for word in [
        "economy", "inflation", "market", "trade", "gdp", "investment",
        "energy", "gas", "oil", "budget", "deficit", "interest rates",
        "zloty", "currency", "exports", "imports", "gospodarka",
        "inflacja", "rynek", "handel", "энергия", "экономика",
        "економіка", "енергія", "経済", "能源", "经济"
    ]):
        return "Economy"

    if any(word in text for word in [
        "eu", "european union", "brussels", "commission",
        "european parliament", "rule of law", "european court",
        "unia europejska", "bruksela", "ue", "евросоюз",
        "євросоюз", "欧洲联盟", "欧州連合"
    ]):
        return "Europe / EU"

    if any(word in text for word in [
        "government", "election", "president", "minister", "parliament",
        "party", "coalition", "opposition", "prime minister", "cabinet",
        "rząd", "wybory", "prezydent", "minister", "parlament",
        "правительство", "выборы", "президент", "уряд", "вибори",
        "政府", "選挙", "选举"
    ]):
        return "Politics"

    if any(word in text for word in [
        "ukraine", "russia", "russian", "putin", "zelensky", "kyiv",
        "moscow", "belarus", "lukashenko", "kremlin", "ukraina",
        "rosja", "białoruś", "украина", "россия", "беларусь",
        "україна", "росія", "білорусь", "ウクライナ", "ロシア",
        "白俄罗斯", "俄罗斯", "乌克兰"
    ]):
        return "Ukraine / Russia / Belarus"

    if any(word in text for word in [
        "migration", "migrant", "refugee", "border crisis", "asylum",
        "migracja", "uchodźcy", "миграция", "беженцы", "міграція",
        "біженці"
    ]):
        return "Migration"

    if any(word in text for word in [
        "china", "chinese", "beijing", "japan", "tokyo", "singapore",
        "asia", "indo-pacific", "chiny", "japonia", "singapur",
        "中国", "日本", "新加坡", "アジア", "日本", "シンガポール"
    ]):
        return "Asia / Indo-Pacific"

    if any(word in text for word in [
        "strategy", "grand strategy", "geopolitics", "foreign policy",
        "international order", "power competition", "great-power",
        "great power", "alliance", "transatlantic", "strategia",
        "geopolityka", "polityka zagraniczna"
    ]):
        return "Foreign Policy / Strategy"

    return "General Poland"


def calculate_importance(article, domain, keyword_group, category):
    score = 0

    score += SOURCE_IMPORTANCE.get(domain, 3)

    if keyword_group in ["politicians", "security_terms"]:
        score += 5
    elif keyword_group == "country_terms":
        score += 3
    else:
        score += 2

    if category in ["Security", "Politics", "Ukraine / Russia / Belarus", "Foreign Policy / Strategy"]:
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


def make_or_query(terms):
    quoted_terms = []

    for term in terms:
        quoted_terms.append(f'"{term}"')

    return " OR ".join(quoted_terms)


def build_query(query_group):
    if query_group == "country_terms":
        important_terms = [
            "Poland", "Polish", "Warsaw",
            "Polska", "Polski", "Warszawa",
            "Polen", "Warschau",
            "Pologne", "Varsovie",
            "Polonia", "Varsovia",
            "Польша", "Польща", "Польшча",
            "波兰", "波蘭", "华沙", "華沙",
            "ポーランド", "ワルシャワ",
            "폴란드", "바르샤바",
            "Polsko", "Lengyelország"
        ]
        return make_or_query(important_terms)

    if query_group == "security_terms":
        return (
            '(Poland OR Polish OR Polska OR Польша OR Польща OR 波兰 OR ポーランド) '
            'AND '
            '(NATO OR security OR military OR defence OR defense OR Ukraine OR Russia OR war)'
        )

    if query_group == "politicians":
        top_politicians = [
            "Donald Tusk",
            "Karol Nawrocki",
            "Radosław Sikorski",
            "Radoslaw Sikorski",
            "Krzysztof Bosak",
            "Andrzej Duda",
            "Jarosław Kaczyński",
            "Jaroslaw Kaczynski",
            "Mateusz Morawiecki",
            "Rafał Trzaskowski",
            "Rafal Trzaskowski",
            "Sławomir Mentzen",
            "Slawomir Mentzen"
        ]

        return (
            '(' + make_or_query(top_politicians) + ') '
            'AND '
            '(Poland OR Polish OR Polska OR Warsaw OR Warszawa OR Польша OR Польща OR 波兰 OR ポーランド)'
        )

    return "Poland OR Polish OR Warsaw"


def search_articles_for_group(media_group_name, domains):
    url = "https://newsapi.org/v2/everything"
    results = []

    domain_string = ",".join(domains)

    query_groups = [
        "country_terms",
        "security_terms",
        "politicians"
    ]

    for query_group in query_groups:
        query = build_query(query_group)

        params = {
            "q": query,
            "domains": domain_string,
            "sortBy": "publishedAt",
            "pageSize": 30,
            "apiKey": API_KEY
        }

        print(f"Searching media group: {media_group_name} | query group: {query_group}")
        print("Query:", query[:250], "...")

        response = requests.get(url, params=params)

        print("Status:", response.status_code)

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

            domain = extract_domain(article_url)

            if not domain:
                domain = domains[0]

            category = categorize_article(title, description)
            people = detect_people(article)
            score = calculate_importance(article, domain, query_group, category)

            results.append({
                "fetched_at": datetime.utcnow().isoformat(),
                "published_at": article.get("publishedAt"),
                "source_type": "Think Tank" if media_group_name == "Think tanks" else "Newspaper / Magazine",
                "media_group": media_group_name,
                "source_domain": domain,
                "source": article.get("source", {}).get("name"),
                "title": title,
                "description": description,
                "url": article_url,
                "keyword": query_group,
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

    for media_group_name, domains in MEDIA_GROUPS.items():
        group_articles = search_articles_for_group(media_group_name, domains)
        new_articles.extend(group_articles)

    all_articles = old_articles + new_articles
    all_articles = remove_duplicates(all_articles)

    all_articles = sorted(
        all_articles,
        key=lambda x: x.get("published_at") or "",
        reverse=True
    )

    print(f"Found {len(new_articles)} new raw articles.")
    print(f"Saved {len(all_articles)} total unique articles.")

    save_articles(all_articles)

    print("Saved articles to data/articles.json")
    print("Finished.")


if __name__ == "__main__":
    main()
