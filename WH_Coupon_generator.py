from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import random
import string
import requests
import json





def openBrowser(url, browser):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser 
    """
    
    print("[INFO] Apertura browser su url \""+url+"\"..."+"\n")
    browser.get(url)
    time.sleep(2)
    
    

    
    
        


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


    #se esiste controlla se nell'array sys.argv in pos 2 esiste un elemento
    try:
      if sys.argv[1]:
         #se esiste recuperalo dal array
        browser_type = sys.argv[1]
        browser = selectBrowser(browser_type)
        

    except:
        #se non esiste chiedi il valore 
        print("[WARNING] Valore \"BROWSER\" non impostato tramite Command Line.\n")
        browser = selectBrowser()
        
    return browser
    
    
def selectBrowser(browser_type = 0):
  
    """Selezione del browser preferito
    """

    if browser_type == "1":
        browser = webdriver.Firefox()
        return browser
    elif browser_type == "2":
        browser = webdriver.Chrome()
        return browser
    else:
        if browser_type != 0:
            print("[ERRORE] Il valore inserito non è corretto.\n")
        browser_type = input("[INPUT] Usare [1]FIREFOX o [2]CHROME: ")
        selectBrowser(browser_type)

        


def main():
    
    # headers = {'Content-Type: application/json'}
    #browser = checkParamCL()
    global auth_token
    
    #Genera una stringa casuale di 15 caratteri per l'email e password
    address = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))+"@emergentvillage.org"
    password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
    
    
    print("[INFO] Generazione email: "+address+"\n")
    print("[INFO] Generazione password: "+password+"\n")
    

    #crea un account con la mail generata e la password
    r = requests.post("https://api.mail.tm/accounts", json={"address": address, "password": password})
    
    json_response = r.json()
    
    
 
    print ("[INFO] ["+ str(r.status_code)+"] "+"["+r.reason+"] Account creato in data: " + json_response['createdAt'] + " con id: " + json_response['id']+"\n")
    
    
    #recupera il token di autenticazione
    r = requests.post("https://api.mail.tm/token", json={"address": address, "password": password})   
    
    json_response = r.json()
    
    auth_token = json_response['token']
    
    print("[INFO] Token recuperato: "+auth_token[:10] + "..."+ auth_token[20:10] +" per l'account con id: "+json_response['id']+"\n")
    
    
    input("[INPUT] Premi un tasto per continuare...")

    #recupera la prima mail 
    r = request.post("https://api.mail.tm/messages/1", headers={"Authorization": "Bearer "+auth_token})
    
    json_response = r.json()

    #recupera il link del coupon

    #scarica il coupon
    
    

    input("Premi Enter per proseguire...")

    

    #apertura browser WH


    openBrowser("https://wienerhaus.it/newsletter", browser)


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
    
    input("Premere un tasto per continuare ................")

    # preme il tasto iscriviti
    submit_elem = browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/form/div[8]/a")
    submit_elem.click()

    print("[SUCCESS] Email registrata!!")

    browser.close()

    print("[SUCCESS] Controlla la casella postale: ", email, ", divertiti con il tuo 15% di sconto")








if __name__ == "__main__":
    main()