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

    "EU media": [
        "lemonde.fr",
        "spiegel.de",
        "bild.de",
        "faz.net",
        "faz.de",
        "politico.eu",
        "mondediplo.com"
    ],

    "Western media": [
        "bbc.com",
        "wsj.com",
        "ft.com",
        "nzz.ch",
        "20min.ch",
        "weltwoche.ch",
        "insideparadeplatz.ch",
        "zerohedge.com",
        "foreignaffairs.com",
        "foreignpolicy.com",
        "thefp.com",
        "thediplomat.com",
        "nationalinterest.org",
        "warontherocks.com",
        "worldpoliticsreview.com",
        "geopoliticalmonitor.com",
        "responsiblestatecraft.org",
        "lawfaremedia.org"
    ],

    "Eastern media": [
        "themoscowtimes.com",
        "kommersant.ru",
        "rbc.ru",
        "vedomosti.ru",
        "novayagazeta.eu",
        "zerkalo.io",
        "charter97.org",
        "belsat.eu",
        "euroradio.fm",
        "reform.news",
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
    "Poland", "Polish", "Warsaw",
    "Polish government", "Polish economy", "Polish security",
    "Polish military", "Poland NATO", "Poland EU", "Poland Ukraine",

    "Polska", "Polski", "Polskę", "Polsce", "Polaków", "Warszawa",
    "rząd Polski", "polska gospodarka", "polskie wojsko", "polskie bezpieczeństwo",

    "Polen", "polnisch", "polnische", "polnischer", "Warschau",
    "polnische Regierung", "polnische Wirtschaft", "polnisches Militär",

    "Pologne", "polonais", "polonaise", "Varsovie",
    "gouvernement polonais", "économie polonaise",

    "Polonia", "polaco", "polaca", "Varsovia", "gobierno polaco",
    "polacco", "polacca", "Varsavia", "governo polacco",
    "Polônia", "polonês", "polonesa", "Varsóvia",

    "Польша", "Польши", "Польшу", "Польше",
    "польский", "польская", "польское", "Варшава",
    "польское правительство", "польская экономика", "польская армия",

    "Польшча", "Польшчы", "Польшчу", "польскі", "польская", "Варшава",

    "Польща", "Польщі", "Польщу",
    "польський", "польська", "польське", "Варшава",
    "польський уряд", "польська економіка", "польська армія",

    "波兰", "波蘭", "华沙", "華沙",
    "波兰政府", "波蘭政府", "波兰经济", "波蘭經濟",
    "波兰军队", "波蘭軍隊",

    "ポーランド", "ポランド", "ワルシャワ",
    "ポーランド政府", "ポーランド経済", "ポーランド軍",

    "폴란드", "바르샤바", "폴란드 정부", "폴란드 경제", "폴란드 군대",

    "Polsko", "polský", "polská", "Varšava",
    "Lengyelország", "lengyel", "Varsó"
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


def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "").lower()
    except Exception:
        return ""


def normalize_domain(domain):
    domain = (domain or "").lower().replace("www.", "")

    if domain.endswith(".onet.pl"):
        return "onet.pl"
    if domain.endswith(".ft.com"):
        return "ft.com"
    if domain.endswith(".bbc.com"):
        return "bbc.com"
    if domain.endswith(".wsj.com"):
        return "wsj.com"
    if domain.endswith(".faz.net"):
        return "faz.net"
    if domain.endswith(".nzz.ch"):
        return "nzz.ch"

    return domain


def article_text(article):
    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""
    url = article.get("url") or ""
    source = article.get("source") or ""
    return f"{title} {description} {content} {url} {source}".lower()


def is_really_about_poland(article):
    text = article_text(article)

    for term in POLAND_TERMS:
        if term.lower() in text:
            return True

    for person in POLITICIANS:
        if person.lower() in text:
            return True

    return False


def is_sports_article(article):
    text = article_text(article)

    sports_terms = [
        "przegladsportowy", "przegląd sportowy", "sport.onet", "sports.onet",
        "sport", "sports", "sportowy", "sportowa", "sportowe",

        "football", "soccer", "match", "matches", "goal", "goals",
        "premier league", "champions league", "europa league",
        "world cup", "fifa", "uefa", "club", "clubs", "transfer", "transfers",
        "striker", "midfielder", "defender", "goalkeeper",
        "coach", "manager", "league", "tournament", "fixture",

        "tennis", "basketball", "volleyball", "skiing", "athletics",
        "formula 1", "f1", "olympics", "olympic",

        "piłka nożna", "pilka nozna", "mecz", "meczu", "bramka", "bramki",
        "gole", "gol", "liga", "ekstraklasa", "transfer", "napastnik",
        "pomocnik", "obrońca", "obronca", "bramkarz", "trener",
        "reprezentacja polski", "zawodnik", "zawodniczka",

        "wisła kraków", "wisla krakow", "legia", "lech poznań", "lech poznan",
        "raków", "rakow", "jagiellonia", "widzew", "pogoń", "pogon",

        "lewandowski", "robert lewandowski", "arkadiusz milik", "milik",
        "zieliński", "zielinski", "szczęsny", "szczesny", "piątek", "piatek",

        "fußball", "fussball", "bundesliga", "tor", "tore", "spieler",
        "trainer", "verein",

        "joueur", "entraîneur", "entraineur", "ligue",

        "футбол", "матч", "гол", "лига", "трансфер", "игрок", "спорт",
        "футболіст", "гравець",

        "足球", "比赛", "比賽", "进球", "進球", "体育", "體育",
        "サッカー", "フットボール", "試合", "ゴール", "スポーツ",
        "축구", "경기", "골", "스포츠"
    ]

    return any(term in text for term in sports_terms)


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
        "中国", "日本", "新加坡", "アジア", "シンガポール"
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


def make_or_query(terms):
    return " OR ".join([f'"{term}"' for term in terms])


def build_query():
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


def search_articles_for_group(media_group_name, domains):
    url = "https://newsapi.org/v2/everything"
    results = []

    domain_string = ",".join(domains)
    query = build_query()

    params = {
        "q": query,
        "domains": domain_string,
        "sortBy": "publishedAt",
        "pageSize": 30,
        "apiKey": API_KEY
    }

    print(f"Searching media group: {media_group_name}")
    print("Query:", query[:250], "...")

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    if response.status_code == 429:
        print("Daily request limit reached.")
        return results

    if response.status_code != 200:
        print("Error:", response.text)
        return results

    data = response.json()

    for article in data.get("articles", []):
        if not is_really_about_poland(article):
            continue

        if is_sports_article(article):
            continue

        title = article.get("title") or ""
        description = article.get("description") or ""
        article_url = article.get("url") or ""

        if not article_url:
            continue

        domain = normalize_domain(extract_domain(article_url))

        if not domain:
            domain = normalize_domain(domains[0])

        category = categorize_article(title, description)
        people = detect_people(article)

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
            "keyword": "country_terms",
            "category": category,
            "people": people
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

    all_articles = [
        article for article in all_articles
        if not is_sports_article(article)
    ]

    all_articles = sorted(
        all_articles,
        key=lambda x: x.get("published_at") or "",
        reverse=True
    )

    print(f"Found {len(new_articles)} new raw articles.")
    print(f"Saved {len(all_articles)} total unique articles after removing sports articles.")

    save_articles(all_articles)

    print("Saved articles to data/articles.json")
    print("Finished.")


if __name__ == "__main__":
    main()
