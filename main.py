from flask import Flask, request, jsonify
import bs4 as bs
from urllib.request import urlopen, Request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/translate', methods=['GET'])
def translate():
    langue1 = request.args.get('langue1')
    langue2 = request.args.get('langue2')
    mot = request.args.get('mot')

    if not langue1 or not langue2 or not mot:
        return jsonify({'error': 'Parameters missing'}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }

    source = f'https://fr.glosbe.com/{langue1}/{langue2}/{mot}'
    req = Request(url=source, headers=headers)
    try:
        html = urlopen(req).read()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    try:
        soup = bs.BeautifulSoup(html, 'lxml')
    except bs.FeatureNotFound:
        soup = bs.BeautifulSoup(html, 'html.parser')

    traductions = []
    exemples = []

    translation_items = soup.find_all('li', {'data-element': 'translation'})
    for item in translation_items:
        translation_phrase = item.find('h3', {'class': 'translation__item__pharse'})
        if translation_phrase:
            traductions.append(translation_phrase.text.strip())

    example_items = soup.find_all('div', {'class': 'px-1 text-sm text-gray-900 break-words'})
    for example in example_items:
        french_div = example.find('div', {'class': 'w-1/2 dir-aware-pr-1'})
        kabyle_div = example.find('div', {'class': 'w-1/2 dir-aware-pl-1'})
        if french_div and kabyle_div:
            french_sentence = french_div.text.strip()
            kabyle_sentence = kabyle_div.text.strip()
            exemples.append((french_sentence, kabyle_sentence))

    return jsonify({'traductions': traductions, 'exemples': exemples})

if __name__ == '__main__':
    app.run(debug=True)
