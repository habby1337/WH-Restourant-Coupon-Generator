from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time


#inizializzazione browser
print("[INFO] Inizializzaizone browser...")
browser = webdriver.Firefox()


def openBrowser(url: string):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser 
    """
    
    print("[INFO] Apertura browser")
    browser.get(url)
    time.sleep(2)

    


#apertura browser su sito web mail 
openBrowser("https://tempail.com/it/")

#recupero mail 


#copia indirizzo mail



#riceve la mail come parametro dalla linea di comando
#email = sys.argv[1]

#email = input(colored('[INPUT]', 'blue')+ " Inserisci l'indirizzo email: ")
#email = input(bcolors.WARNING + "[INPUT]" + " Inserisci l'indirizzo email: " + bcolors.OKBLUE)

email = input("[INPUT] Inserisci l'indirizzo email: ")



print("[INFO] Apertura browser")

openBrowser("https://wienerhaus.it/newsletter")


print("[INFO] Inserimento valori nei rispettivi campi")

name_filed_elem = browser.find_element(By.NAME, "firstname") #ricerca il campo nome
surname_field_elem = browser.find_element(By.NAME, "lastname") #ricerca il campo cognome
email_field_elem = browser.find_element(By.NAME, "email")#ricera il campo email

name_filed_elem.clear()
name_filed_elem.send_keys("luca") #inserice il nome nel campo nome

surname_field_elem.clear()
surname_field_elem.send_keys("luchetti") #inserisce il cognome nel campo congome

#inserisce la mail presa da linea di comando
email_field_elem.clear()
email_field_elem.send_keys(email)

print("[SUCCESS] Valori inseriti!")


print("[INFO] PRicerca tasto per i coockies")
#chiude i cookies
cookie_elem = browser.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

print("[SUCCESS] Chiusura de sti cookies del cavolo")
time.sleep(1)

#clicca sul link informativa privacy

print("[INFO] E leggiamo sta privacy... vah")

privacy_popup_button_elem = browser.find_element(By.LINK_TEXT,"informativa privacy")
privacy_popup_button_elem.click()



time.sleep(2)



#chiude il popup
privacy_popup_elem = browser.find_element(By.XPATH, "/html/body/div[7]/div/div/a")
privacy_popup_elem.click()

print("[SUCCESS] Privacy letta e imparata a memoria :)")

time.sleep(1)

print("[INFO] Ricerca tasto per iscrizione")

# preme il tasto iscriviti
submit_elem = browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/form/div[8]/a")
submit_elem.click()

print("[SUCCESS] Email registrata!!")

browser.close()

print("[SUCCESS] Controlla la casella postale: ", email, ", divertiti con il tuo 15% di sconto")


