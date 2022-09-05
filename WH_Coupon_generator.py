import sys
import time
import random
import string
import requests
import json
import re
import os
import errno

from selenium import webdriver
# Importa il sistema di tasti da selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Importa il sistema di ricerca
# Importa le opzioni per il browser
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.action_chains import ActionChains  # Importa le azioni


from colorama import init
from colorama import Fore, Back, Style

from termcolor import colored


# TODO utilizzare un altro sistema di mail in modo da avere un ampio raggio di domini da poter utilizzare per evitare di avere blocchi futuri
# TODO rimuovere tutto il codice inutile commentato
# TODO Pulizzia del codice, formattazione e aggiunta commenti
# TODO Implementare timestamp dei processi eseguiti

def sendMessage(message, type):
    """Invio messaggio a schermo con colore diverso a seconda del tipo di messaggio

    Args:
        message (string): Messaggio da inviare a schermo
        type (string): Tipo di messaggio da inviare a schermo
    """

    if type == "error":
        print(colored("[ERROR]", "red") + " " + message)
    elif type == "info":
        print(colored("[INFO]", "cyan") + " " + message)
    elif type == "success":
        print(colored("[SUCCESS]", "green") + " " + message)
    elif type == "warning":
        print(colored("[WARNING]", "yellow") + " " + message)
    elif type == "input":
        return input(colored("[INPUT]", "on_magenta") + " " + message)
    elif type == "nope":
        print(colored("[NOPE]", "on_red") + " " + message)
    elif type == "found":
        print(colored("[FOUND]", "on_green") + " " + message)
    elif type == "phase":
        print("\n" + colored("[##########]", "on_grey") + " " +
              message + " " + colored("[##########]", "on_grey") + "\n")
    else:
        print("[*]" + message)


def openBrowser(url, browser):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser 
    """

    sendMessage("Apertura browser su url \""+url+"\"...", "info")
    browser.get(url)
    # time.sleep(2) #attesa per caricamento pagina (non necessario )


def checkParamCL():
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


def selectBrowser(browser_type=0):
    """Selezione del browser preferito
    """

    if browser_type == "1":
        op = Options()
        op.add_argument("--headless")
        browser = webdriver.Firefox(options=op)
        return browser
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
    """Controllo se l'email è arrivata
    """
    sendMessage("[INFO] Controllo se l'email è arrivata...", "info")

    # recupera la lista di mail ricevute
    r = requests.get("https://api.mail.tm/messages",
                     headers={"Authorization": "Bearer "+auth_token})
    json_response = r.json()

    if json_response['hydra:totalItems'] == 0:
        sendMessage(
            "Nessuna email ricevuta, Aspetto 5 secondi e tento nuovamente.", "nope")
        time.sleep(5)
        return checkRecivedEmail()
    else:
        json_response = json_response['hydra:member'][0]

        sendMessage("Mail ricevuta: ", "found")

        print("\n" + colored("[*]", "white", attrs=["bold"]) + "Id: " + json_response['id'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Mittente: " + json_response['from']['name'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Oggetto: " + json_response['subject'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Data: " + json_response['createdAt'] +
              "\n" + colored("[*]", "white", attrs=["bold"]) + "Download link: " + json_response['downloadUrl'] + "\n")

        mail_id = json_response['id']
        return mail_id


def main():
    init()  # inizializza colorama per stampare a colori

    # os.system('color') vecchio sistema di utilizzo colori

    browser = checkParamCL()
    global auth_token

    # Genera una stringa casuale di 15 caratteri per l'email e password

    address = ''.join(random.choices(string.ascii_lowercase +
                      string.digits, k=15))+"@emergentvillage.org"
    password = ''.join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))

    # address = "ao13vfntvdbhl1k@emergentvillage.org"
    # password = "h0eT8QIbRp"

    sendMessage("FASE 1 => GENERAZIONE ACCOUNT EMAIL TEMPORANEA", "phase")
    sendMessage("Generazione Email: " + address, "info")
    sendMessage("Generazione Password: " + password, "info")

    # crea un account con la mail generata e la password

    r = requests.post("https://api.mail.tm/accounts",
                      json={"address": address, "password": password})

    json_response = r.json()

    account_id = json_response['id']

    sendMessage("[" + str(r.status_code)+"] "+"["+r.reason+"] Account creato in data: " +
                json_response['createdAt'] + " con id: " + json_response['id']+"\n", "success")

    # print("[SUCCESS] [" + str(r.status_code)+"] "+"["+r.reason+"] Account creato in data: " +
    #       json_response['createdAt'] + " con id: " + json_response['id']+"\n")

    sendMessage("FASE 2 => RIEMPIMENTO FORM WIENER HAUS", "phase")
    # apertura browser WH
    openBrowser("https://wienerhaus.it/newsletter", browser)

    sendMessage("Insermiento valori nei rispettivi campi", "info")

    # Richiesta per generazione nome e cognome

    r = requests.get("https://randomuser.me/api/?inc=name&nat=de&result=1")

    name = r.json()['results'][0]['name']['first']
    surname = r.json()['results'][0]['name']['last']

    name_filed_elem = browser.find_element(
        By.NAME, "firstname")  # ricerca il campo nome
    surname_field_elem = browser.find_element(
        By.NAME, "lastname")  # ricerca il campo cognome
    email_field_elem = browser.find_element(
        By.NAME, "email")  # ricera il campo email

    name_filed_elem.clear()
    # inserice il nome nel campo nome
    name_filed_elem.send_keys(name)

    surname_field_elem.clear()
    # inserisce il cognome nel campo congome

    surname_field_elem.send_keys(surname)

    # inserisce la mail presa da linea di comando
    email_field_elem.clear()
    email_field_elem.send_keys(address)

    sendMessage("Valori inseriti!", "success")

    sendMessage("FASE 3 => CHIUSURA DI TUTTI I VARI POPUP", "phase")

    sendMessage("Ricerca tasto per i cookies", "info")

    # chiude i cookies
    cookie_elem = browser.find_element(
        By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

    sendMessage("Chiusura de sti cookies del cavolo", "success")

    time.sleep(1)

    # clicca sul link informativa privacy

    sendMessage("Lettura della privacy... o almeno facendo finta", "info")

    privacy_popup_button_elem = browser.find_element(
        By.LINK_TEXT, "informativa privacy")
    privacy_popup_button_elem.click()

    time.sleep(2)

    # chiude il popup
    privacy_popup_elem = browser.find_element(
        By.XPATH, "/html/body/div[7]/div/div/a")
    privacy_popup_elem.click()

    sendMessage("Privacy letta e imparata a memoria >:)", "success")

    time.sleep(1)

    sendMessage("Ricerca tasto per iscrizione ", "info")

    # preme il tasto iscriviti
    submit_elem = browser.find_element(
        By.XPATH, "/html/body/div[3]/div[1]/div/form/div[8]/a")
    submit_elem.click()

    sendMessage("Iscrizione effettuata con successo", "success")

    sendMessage("Controlla la casella postale: " + address +
                ", Divertiti con il tuo 15% di socnto", "success")

    sendMessage("FASE 4 => RECUPERO EMAIL CON IL CODICE COUPON", "phase")

    # recupera il token di autenticazione
    r = requests.post("https://api.mail.tm/token",
                      json={"address": address, "password": password})
    json_response = r.json()

    auth_token = json_response['token']

    sendMessage("Token recuperato: " + auth_token[:5] + "..." + auth_token[20:25] +
                " per l'account con id: " + json_response['id'], "success")

    # recupera la mail ricevuta
    message_id = checkRecivedEmail()

    r = requests.get("https://api.mail.tm/messages/"+message_id,
                     headers={"Authorization": "Bearer "+auth_token})
    json_response = r.json()

    # Ricarca il link del coupon
    m = re.search(
        "\[https://wienerhaus\.it/newsletter/confirm\?key=(.+?)]", json_response['text'])

    link_coupon = m.group(1)

    sendMessage("Chiave del coupon: " + link_coupon + "\n " + colored("[*]", "white", attrs=[
                "bold"]) + "Link del coupon: https://wienerhaus.it/newsletter/confirm?key="+link_coupon, "success")

    # apre il browser e va alla pagina del coupon
    openBrowser("https://wienerhaus.it/newsletter/confirm?key=" +
                link_coupon, browser)

    browser.find_element(By.XPATH, "/html/body/div[2]/div/a").click()

    # switcha alla nuova scheda con il coupon
    browser.switch_to.window(browser.window_handles[1])

    # recupero imagine coupon
    time.sleep(2)

    sendMessage("FASE 5 => SALVATAGGIO COUPON", "phase")

    # try:
    #     os.remove("geckodriver.log")
    #     os.remove("coupon.png")
    #     print("[INFO] Rimozione file temporanei e coupon vecchi")
    # except OSError:
    #     pass

    sendMessage("Salvataggio immagine coupon --> coupon.png", "info")
    # browser.save_full_page_screenshot("coupon.png")

    # Invia il tasto END per scendere in fondo
    actions = ActionChains(browser)
    actions.send_keys(Keys.END).perform()

    time.sleep(2)
    browser.save_full_page_screenshot("coupon.png")

    sendMessage("Coupon salvato!", "success")

    sendMessage("Eliminazione account email temporaneo", "info")

    r = requests.delete("https://api.mail.tm/accounts/"+account_id,
                        headers={"Authorization": "Bearer "+auth_token})


    print("\n\n\n\n\n\n....\n....\n...\n..\n.\nBye Bye >:D\n\n\n")

    input("Premi un tasto per chiudere il programma")

    browser.quit()


if __name__ == "__main__":
    main()
