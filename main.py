import bs4 as bs
from urllib.request import urlopen, Request

def scrape_and_translate(langue1, langue2, mot):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }

    source = f'https://fr.glosbe.com/{langue1}/{langue2}/{mot}'
    print(f"Scraping URL: {source}")

    req = Request(url=source, headers=headers)
    try:
        html = urlopen(req).read()
    except Exception as e:
        print(f"Failed to retrieve webpage: {e}")
        return None

    # Try to use 'lxml' parser, if not available fall back to 'html.parser'
    try:
        soup = bs.BeautifulSoup(html, 'lxml')
    except bs.FeatureNotFound:
        soup = bs.BeautifulSoup(html, 'html.parser')

    traductions = []
    exemples = []

    translation_items = soup.find_all('li', {'data-element': 'translation'})
    for item in translation_items:
        translation_phrase = item.find('h3', {'class': 'translation__item__pharse'}).text.strip()
        traductions.append(translation_phrase)

    example_items = soup.find_all('div', {'class': 'px-1 text-sm text-gray-900 break-words'})
    for example in example_items:
        french_sentence = example.find('div', {'class': 'w-1/2 dir-aware-pr-1'}).text.strip()
        kabyle_sentence = example.find('div', {'class': 'w-1/2 dir-aware-pl-1'}).text.strip()
        exemples.append((french_sentence, kabyle_sentence))

    return traductions, exemples

# Exemple d'utilisation de la fonction
langue1 = 'fr'
langue2 = 'kab'
mot = 'lion'

traductions, exemples = scrape_and_translate(langue1, langue2, mot)
print(f"Traductions pour '{mot}': {traductions}")
if exemples:
    print(f"Exemples de phrases :")
    for fr, kab in exemples:
        print(f"Français : {fr}")
        print(f"Kabyle : {kab}")
else:
    print("Aucun exemple de phrase disponible")
