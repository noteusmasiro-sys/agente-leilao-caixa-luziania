import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL_BUSCA = "https://venda-imoveis.caixa.gov.br/sistema/venda-imoveis/busca"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload)

def buscar_imoveis():
    r = requests.get(URL_BUSCA, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select(".card-imovel")
    encontrados = []

    for card in cards:
        texto = card.get_text(" ").lower()

        if "luziânia" in texto and "usado" in texto:
            link = card.find("a")
            if link and link.get("href"):
                encontrados.append(
                    "https://venda-imoveis.caixa.gov.br" + link["href"]
                )

    return encontrados

def main():
    imoveis = buscar_imoveis()

    if imoveis:
        msg = "🏠 Imóveis USADOS em leilão - Luziânia/GO\n\n"
        for i in imoveis:
            msg += f"{i}\n"
        enviar_telegram(msg)

if __name__ == "__main__":
    main()
