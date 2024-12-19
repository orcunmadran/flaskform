import os

from flask import Flask, send_file, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/arama")
def arama():
    sozluk = {"apple":"elma", "karpuz":"water melon", "kavun":"melon"}
    anahtarKelime = request.args.get('anahtarKelime','')
    if anahtarKelime in sozluk:
        anahtarKelime = sozluk[anahtarKelime]
    else:
        anahtarKelime = "Aradığınız meyve sözlükte yok!"
    return render_template('arama.html', data=anahtarKelime)

@app.route("/katalog")
def katalog():
    
    tree = ET.parse('katalog.xml')
    root = tree.getroot()

    catalog = []
    for cd in root.findall('CD'):
        cd_dict = {}
        for child in cd:
            cd_dict[child.tag] = child.text
        catalog.append(cd_dict)

    # Eğer bir arama yapılmışsa, anahtar kelimeye göre filtrele
    if request.method == "GET":
        keyword = request.args.get("anahtarKelime", "").lower()
        filtered_catalog = [
            cd for cd in catalog if any(keyword in (v or "").lower() for v in cd.values())
        ]
        return render_template("katalog.html", data=filtered_catalog)    

    return render_template("katalog.html", data=catalog)


def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
