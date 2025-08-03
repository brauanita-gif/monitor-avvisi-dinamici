import time
import smtplib
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

# Setup Chrome per Render
chromedriver_autoinstaller.install()
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Siti da monitorare
urls = [
    "https://www.portaleargo.it/albopretorio/online/#/?customerCode=SC24478",
    "https://www.portaleargo.it/albopretorio/online/#/?customerCode=SC27334",
    "https://web.spaggiari.eu/sdg2/AlboOnline/NUME0013"
]

# Parole chiave
keywords = [
    "Avviso", "Manifestazione", "Interesse", "Interpello", "Progetto",
    "Mediazione Linguistica e Culturale", "Mediazione Culturale", "Mediazione Linguistica",
    "Mediazione Interculturale", "Mediatore Linguistico Culturale", "Mediatore Culturale",
    "Mediatore Linguistico", "Mediatore Interculturale", "Lingue", "Facilitatore Linguistico",
    "Inglese", "Francese", "Lingua Inglese", "Lingua Francese"
]

# Email config
sender_email = "brauanita@gmail.com"
receiver_email = "brauanita@gmail.com"
password = "taad hlvr tzrc qnoj"

def send_email(subject, body):
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver_email, message)

found_announcements = []

# Visita ogni sito e cerca parole chiave
for url in urls:
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        text = soup.get_text()
        for keyword in keywords:
            if keyword.lower() in text.lower():
                found_announcements.append((url, keyword))
                break
    except Exception as e:
        print(f"Errore con {url}: {e}")

driver.quit()

# Invia email se ci sono risultati
if found_announcements:
    body = "\n".join([f"{kw} trovato in: {u}" for u, kw in found_announcements])
    send_email("🔔 Avviso trovato!", body)
