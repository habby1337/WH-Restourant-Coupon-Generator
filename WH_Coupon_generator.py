import sys
import time
import random
import string
import requests
import json
import re
import os
import errno
import datetime
import telepot
import socket
import logging


from selenium import webdriver
# Importa il sistema di tasti da selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Importa il sistema di ricerca
# Importa le opzioni per il browser
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.action_chains import ActionChains  # Importa le azioni

from selenium.webdriver.common.proxy import Proxy, ProxyType  # Proxy

# importa il necessario per il colore su terminale
from colorama import init

from termcolor import colored

import config


# CONFIGURAZIONE TELEGRAM
telegram_bot_api_key = config.telelgram_bot_api_key
telegram_chat_id = config.telegram_chat_id

person_name = ""
person_surname = ""
working_path = os.getcwd()  # recupera il path di lavoro

# TODO Aggiungere generazione log per le operazioni
# TODO Spostare le funzioni in file separati
# FIXME Migliorare i tempi di esecuzione e attesa


def sendMessage(message, type):
    """Invio messaggio a schermo con colore diverso a seconda del tipo di messaggio

    Args:
        message (string): Messaggio da inviare a schermo
        type (string): Tipo di messaggio da inviare a schermo
    """

    if type == "error":
        print(getTimestamp() + colored("[ERROR]", "red") + " " + message)
    elif type == "info":
        print(getTimestamp() + colored("[INFO]", "cyan") + " " + message)
    elif type == "success":
        print(getTimestamp() + colored("[SUCCESS]", "green") + " " + message)
    elif type == "warning":
        print(getTimestamp() + colored("[WARNING]", "yellow") + " " + message)
    elif type == "input":
        return input(colored("[INPUT]", "white", "on_magenta") + " " + message)
    elif type == "nope":
        print(getTimestamp() + colored("[NOPE]",
              "white", "on_red") + " " + message)
    elif type == "found":
        print(getTimestamp() + colored("[FOUND]",
              "white", "on_green") + " " + message)
    elif type == "phase":
        print("\n" + colored("[##########] ", "white", "on_grey") + " " +
              message + " " + colored(" [##########]", "white", "on_grey") + "\n")
    else:
        print(getTimestamp() + "[*] " + message)


def getTimestamp():
    """Scrive il timestamp corrente

    Returns:
        timestamp: timestamp elaborato
    """
    now = datetime.datetime.now()
    return "[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] "


def openBrowser(url, browser):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser
    """

    # TODO Aggiungere il logging delle attivita della funzione

    sendMessage("Apertura browser su url \""+url+"\"...", "info")
    browser.get(url)
    # time.sleep(2) #attesa per caricamento pagina (non necessario )


def checkParamCL():
    """Controlla se sono stati impostati dei valori nei parametri di avvio tramite command line del programma

    Returns:
        object: IL browser selezionato
    """
    # HACK saltata verifica parametri da linea di comando
    # TODO Migliormaneto attributi inseriti nella comand line / migliorare il sistema con cui si passano i due attributi
    # TODO Aggiungere il logging delle attivita della funzione

    # -[x] verifica parametro del browser
    # try:
    #     #controlla se nell'array sys.argv in pos 1 esiste un elemento
    #     if sys.argv[1]:

    #         #se esiste recuperalo dal array
    #         email = sys.argv[1]
    # except:
    #     #se non esiste chiedi il valore
    #     print("[WARNING] Valore \"EMAIL\" non impostato tramite Command Line.\n")
    #     email = input("[INPUT] Inserisci l'indirizzo email: ")

    # se esiste controlla se nell'array sys.argv in pos 2 esiste un elemento
    try:
        if sys.argv[1]:
           # se esiste recuperalo dal array
            browser_type = sys.argv[1]
            browser = selectBrowser(browser_type)

    except:
        # se non esiste chiedi il valore

        sendMessage(
            " Valore \"BROWSER\" non impostato tramite Command Line.\n", "warning")
        browser = selectBrowser()

    return browser


def getProxyIP():
    """Recupera una lista di proxy da api pubblica e ne ritorna il primo con il ping minore

    Returns:
        sting: ip:porta del proxy con il ping minore
    """

    # TODO Aggiungere il logging delle attivita della funzione

    sendMessage("Recupero lista proxy dalle API pubbliche...", "info")

    r = requests.get(
        "https://www.proxyscan.io/api/proxy?last_check="+config.ProxySettings["last_check"]+"&country="+config.ProxySettings["country"]+"&uptime="+config.ProxySettings["uptime"]+"&ping="+config.ProxySettings["ping"]+"&limit=1&type=socks5").json()

    if not r:
        sendMessage("Nessun proxy disponibile, tento nuovamente...", "warning")
        return getProxyIP()
    else:
        sendMessage(
            "Proxy disponibili! Selezionato il: " + str(r[0]["Ip"])+":"+str(r[0]["Port"]) + ". Verifico che sia ONLINE...", "success")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((str(r[0]["Ip"]), r[0]["Port"]))

        if result == 0:
            sendMessage("Proxy trovato: "+str(r[0]
                        ["Ip"])+":"+str(r[0]["Port"]) + ". Utilizzo questo... ", "success")
            return str(r[0]["Ip"]) + ":" + str(r[0]["Port"])
        else:
            sendMessage(
                "Il Proxy recuperato risulta OFFLINE, nuova ricerca...", "warning")
            return getProxyIP()


def selectBrowser(browser_type="1"):  # HACK il valore deve essere 0 senza virgolette
    """Seleziona il browser da utilizzare e applica le impostazioni Proxy, Headless e UserAgent

    Args:
        browser_type (int, optional): valore per la selezione tra Firefox = 1 o Chrome = 2. Defaults to 0.

    Returns:
        object: browser selezionato
    """
    # TODO Aggiungere il logging delle attivita della funzione
    if browser_type == "1":
        op = Options()
        op.add_argument("--headless")

        PROXY = getProxyIP()

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXY,
            'ftpProxy': PROXY,
            'sslProxy': PROXY,
            'noProxy': 'None'  # set this value as desired
        })

        sendMessage("Inizializzazione browser...", "info")
        try:
            browser = webdriver.Firefox(
                options=op, proxy=proxy)
            sendMessage("Browser inizializzato!", "success")
            return browser
        except Exception as e:
            sendMessage(
                "Errore durante l'inizializzazione del browser(Visualizza i log per l'errore completo) , Provo nuovamente..", "error")
            logging.error(
                "Errore durante l'inizializzazione del browser: "+str(e))
            return selectBrowser("1")

    elif browser_type == "2":
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        browser = webdriver.Chrome(options=op)
        return browser
    else:
        if browser_type != 0:
            sendMessage("Il valore inserito non è corretto.\n", "error")
        browser_type = sendMessage("Usare [1]FIREFOX o [2]CHROME: ", "input")
        selectBrowser(browser_type)


def checkRecivedEmail():
    """Controlla se all'indirizzo generato è arrivata la mail di conferma

    Returns:
        mail_id: identificativo della mail di conferma
    """
    sendMessage(" Controllo se l'email è arrivata...", "info")
    logging.info("Controllo se l'email è arrivata...")

    # recupera la lista di mail ricevute
    r = requests.get(
        "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email_username + "&domain=" + email_domain)

    list_of_emails = r.json()

    # controlla se la lista è vuota
    if len(list_of_emails) == 0:
        sendMessage(
            "Nessuna email ricevuta, Aspetto 5 secondi e tento nuovamente.", "nope")
        logging.warning("Nessuna email ricevuta, in attesa...")
        time.sleep(5)
        # richiama la funzione per controllare se la lista è vuota
        return checkRecivedEmail()
    else:
        # se la lista non è vuota recupera  la prima mail
        json_response = list_of_emails[0]

        sendMessage(" Mail ricevuta: ", "found")
        logging.info("Mail ricevuta, ID: " + str(json_response['id']))

        print("\n" + colored("[*]", "white", attrs=["bold"]) + "Id: " + str(json_response['id']) +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Mittente: " + json_response['from'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Oggetto: " + json_response['subject'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Data: " + json_response['date'])

        mail_id = json_response['id']
        return mail_id  # ritorna l'id della mail


def getEmailDomain():
    """Richiesta alle api di 1secmail per i domini disponibili

    Returns:
        email_domain: ritorna un dominio casuale tra i domini disponibili
    """

    logging.info("Recupero lista domini disponibili...")
    r = requests.get("https://www.1secmail.com/api/v1/?action=getDomainList")
    email_domains = r.json()

    return email_domains[random.randint(0, len(email_domains)-1)]


def sendTelegramMessage(chat_id, pdf_coupon_link):
    """Invia l'immagine e il link del coupon tramite la chat telegram passata come parametro

    Args:
        chat_id (string): identificativo della chat a cui mandare il messaggio
        pdf_coupon_link (string): codice generato del coupon
    """

    logging.info("Invio immagine coupon.png tramite Telegram...")

    bot = telepot.Bot(telegram_bot_api_key)

    logging.info("Creazione istanza Bot Telegram...")

    logging.info("Invio link coupon tramite Telegram...")

    try:
        logging.info("Prova invio messaggio su telegram.")
        bot.sendPhoto(chat_id=chat_id, photo=open('STARTERS/coupon.png', 'rb'),
                      caption="✳ **W**iener **H**aus *Coupon* *Generator* ✳\n*☺ Coupon Generato Correttamente ✅*\n\n 🌐 Link PDF: [Clicca qui](https://wienerhaus.it/newsletter/confirm?key=" +
                      pdf_coupon_link + ")",
                      parse_mode='MarkdownV2')
        sendMessage("Messaggio inviato correttamente", "success")
        logging.info("Messaggio inviato correttamente")
    except Exception as e:
        sendMessage("Errore nell'invio del messaggio", "error")
        logging.error("Errore nell'invio del messaggio: " + str(e))


def getRandomPerson():
    """Recupera un nominativo casuale da un url api (json) https://randomuser.me/

    """

    try:
        sendMessage("Sto generando Nome e Cognome...", "info")
        # Richiesta per generazione nome e cognome da fonte api
        r = requests.get("https://randomuser.me/api/?inc=name&nat=de&result=1")
        global person_name, person_surname
        person_name = r.json()['results'][0]['name']['first']
        person_surname = r.json()['results'][0]['name']['last']
    except Exception as e:
        sendMessage(
            "Errore nella generazione del nome e cognome, sto tentando nuovamente", "nope")
        logging.error("Errore generazione nome e cognome")
        return getRandomPerson()


def cleanOldFiles():
    logging.info("Inizio rimozione file vecchi")
    sendMessage("Rimozione file vecchi...", "info")
    # Pulizzia file vecchi (coupon e log)
    try:
        logging.info("Rimozione file \"coupon.png\"")
        os.remove(working_path + "\coupon.png")
        sendMessage(
            "Il file coupon.png esisteva, allora è stato cancellato...", "scuccess")
    except OSError:
        logging.error("Il file \"coupon.png\" non esiste")
        sendMessage(
            "Il file coupon.png non esiste, quindi non serve cancellarlo...", "info")

    try:
        logging.info("Rimozione file \"log.txt\"")
        os.remove(working_path + "\geckodriver.log")
        sendMessage(
            "Il file geckodriver.log esisteva, allora è stato cancellato...", "scuccess")
    except OSError:
        logging.error("Il file \"geckodriver.log\" non esiste")
        sendMessage(
            "Il file geckodriver.log non esiste, quindi non serve cancellarlo...", "info")

    try:
        logging.info("Rimozione file \"WH-LOG.log\"")
        os.remove(working_path + "\WH-LOG.log")
        sendMessage(
            "Il file WH-LOG.log esisteva, allora è stato cancellato...", "scuccess")
    except OSError:
        logging.error("Il file \"WH-LOG.log\" non esiste")
        sendMessage(
            "Il file WH-LOG.log non esiste, quindi non serve cancellarlo...", "info")

    logging.info("Rimozione file completata")
    sendMessage("Rimozione file completata", "success")


def main():
    logging.basicConfig(filename='WH-LOG.log', level=logging.INFO, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', encoding='utf-8', force=True)

    # GUI.GUI()  # Inizializa la gui
    sendMessage("FASE 0 => RIMOZIONE FILE VECCHI", "phase")
    cleanOldFiles()

    logging.info("Inizio esecuzione script")
    init()  # inizializza colorama per stampare a colori

    logging.info("Inizializzazione browser")
    # Crea l'oggetto browser
    browser = checkParamCL()

    logging.info("Inizio procedura di registrazione")

    global email_username
    global email_domain

    logging.info("Generazione indirizzo email")

    # Genera una stringa casuale di 15 caratteri per l'email e password
    email_domain = getEmailDomain()

    email_username = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

    address = email_username+"@" + email_domain

    logging.info("Indirizzo email generato: " + address)

    sendMessage("FASE 1 => GENERAZIONE ACCOUNT EMAIL TEMPORANEA", "phase")
    sendMessage("Generazione Email: " + address, "success")

    sendMessage("FASE 2 => RIEMPIMENTO FORM WIENER HAUS", "phase")

    logging.info("Apertura pagina di registrazione")

    # apertura browser WH
    openBrowser("https://wienerhaus.it/newsletter", browser)

    sendMessage("Insermiento valori nei rispettivi campi", "info")

    logging.info("Generazione nome e cognome casuale")

    getRandomPerson()  # Recpuera nome e cognome casuale

    name_filed_elem = browser.find_element(
        By.NAME, "firstname")  # ricerca il campo nome
    surname_field_elem = browser.find_element(
        By.NAME, "lastname")  # ricerca il campo cognome
    email_field_elem = browser.find_element(
        By.NAME, "email")  # ricera il campo email

    # pulisce e inserice il nome nel campo nome
    name_filed_elem.clear()
    name_filed_elem.send_keys(person_name)

    logging.info("Nome inserito: " + person_name)

    # pulisce e inserisce il cognome nel campo congome
    surname_field_elem.clear()
    surname_field_elem.send_keys(person_surname)

    logging.info("Cognome inserito: " + person_surname)

    sendMessage("Nome e cognome generati, Si chiama: " +
                person_name + " " + person_surname, "success")

    # inserisce la mail presa da linea di comando
    email_field_elem.clear()
    email_field_elem.send_keys(address)

    logging.info("Email inserita: " + address)

    logging.info("Inserimento valori completato")

    sendMessage("Valori inseriti!", "success")
    sendMessage("FASE 3 => CHIUSURA DI TUTTI I VARI POPUP", "phase")
    sendMessage("Ricerca tasto per i cookies", "info")

    logging.info("Ricerca tasto per i cookies")
    # chiude i cookies
    cookie_elem = browser.find_element(
        By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

    logging.info("Tasto cookies trovato e chiuso")

    sendMessage("Chiusura de sti cookies del cavolo", "success")

    time.sleep(1)

    # clicca sul link informativa privacy
    logging.info("Ricerca tasto per la privacy")

    sendMessage("Lettura della privacy... o almeno facendo finta", "info")

    privacy_popup_button_elem = browser.find_element(
        By.LINK_TEXT, "informativa privacy")
    privacy_popup_button_elem.click()

    time.sleep(2)

    # chiude il popup
    privacy_popup_elem = browser.find_element(
        By.XPATH, "/html/body/div[7]/div/div/a")
    privacy_popup_elem.click()

    logging.info("Tasto privacy trovato e chiuso")

    sendMessage("Privacy letta e imparata a memoria >:)", "success")

    time.sleep(1)

    logging.info("Ricerca tasto per la newsletter")

    sendMessage("Ricerca tasto per iscrizione ", "info")

    # preme il tasto iscriviti
    submit_elem = browser.find_element(
        By.XPATH, "/html/body/div[3]/div[1]/div/form/div[8]/a")
    submit_elem.click()

    logging.info("Tasto iscrizione trovato e premuto")

    sendMessage("Iscrizione effettuata con successo", "success")

    sendMessage("Controlla la casella postale: " + address +
                ", Divertiti con il tuo 15% di socnto", "success")

    sendMessage("FASE 4 => RECUPERO EMAIL CON IL CODICE COUPON", "phase")

    logging.info("Inizio procedura di recupero email con codice sconto")
    # recupera la mail ricevuta
    email_id = checkRecivedEmail()

    logging.info("Recupero email completato")

    r = requests.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" +
                     email_username + "&domain=" + email_domain + "&id=" + str(email_id))

    json_response = r.json()['htmlBody']

    logging.info("Recupero codice sconto")

    # Ricarca il link del coupon
    m = re.search(
        "https://wienerhaus\.it/newsletter/confirm\?key=(.+?)'", json_response)

    link_coupon = m.group(1)

    logging.info("Codice sconto recuperato: " + link_coupon)

    sendMessage("Chiave del coupon: " + link_coupon + "\n " + colored("[*]", "white", attrs=[
                "bold"]) + "Link del coupon: https://wienerhaus.it/newsletter/confirm?key="+link_coupon, "success")

    # apre il browser e va alla pagina del coupon
    openBrowser("https://wienerhaus.it/newsletter/confirm?key=" +
                link_coupon, browser)

    logging.info("Apertura pagina del coupon")

    browser.find_element(By.XPATH, "/html/body/div[2]/div/a").click()

    # switcha alla nuova scheda con il coupon
    browser.switch_to.window(browser.window_handles[1])

    logging.info("Switch alla nuova scheda")

    # recupero imagine coupon
    time.sleep(2)

    sendMessage("FASE 5 => SALVATAGGIO COUPON", "phase")

    logging.info("Inizio salvataggio coupon")
    sendMessage("Salvataggio immagine coupon --> coupon.png", "info")

    # Invia il tasto END per scendere in fondo
    actions = ActionChains(browser)
    actions.send_keys(Keys.END).perform()

    time.sleep(2)
    browser.save_full_page_screenshot("coupon.png")

    logging.info("Salvataggio coupon completato > coupon.png")
    # Invia messaggio tramite telegram
    sendTelegramMessage(telegram_chat_id, link_coupon)  # Chat id

    sendMessage("Coupon salvato!", "success")

    sendMessage("Eliminazione account email temporaneo", "info")
    logging.info("Eliminazione account email temporaneo")

    # Uscita dal programma con stile
    for item in 5, 4, 3, 2, 1:
        print(colored("[GOODBYE]", "magenta", attrs=["underline", "bold"]) + " Programma terminato in " +
              colored("  " + str(item) + "  ", "magenta", "on_white", attrs=["bold"],) + " secondi" + colored(" [GOODBYE]", "magenta", attrs=["underline", "bold"]) + "\r", end="")
        time.sleep(1)

    logging.info("Programma terminato")
    os.system("cls")

    print(colored("[EXIT] Bye Bye >:D\n\n\r", "magenta", attrs=["bold"]))

    input(colored("[INPUT]", "yellow", attrs=["bold"]) + " Premi " + colored("[ ENTER ]", "white",
                                                                             "on_green", attrs=["bold"]) + " per chiudere il programma...")

    browser.quit()


if __name__ == "__main__":
    main()
