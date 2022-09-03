from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import random
import string
import requests
import json
import re





def openBrowser(url, browser):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser 
    """
    
    print("[INFO] Apertura browser su url \""+url+"\"...")
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



def checkRecivedEmail():
    """Controllo se l'email è arrivata
    """
    print("\n[INFO] Controllo se l'email è arrivata...")
    
    #recupera la lista di mail ricevute
    r = requests.get("https://api.mail.tm/messages", headers={"Authorization": "Bearer "+auth_token})
    json_response = r.json()

    
    if json_response['hydra:totalItems'] == 0:
        print("[NOPE] Nessuna email ricevuta, Aspetto 5 secondi e tento nuovamente.")
        time.sleep(5)
        return checkRecivedEmail()
    else:
        json_response = json_response['hydra:member'][0]
    
        print("[FOUND] Mail ricevuta: " +
            "\n[*]Id: "+ json_response['id']+
            "\n[*]Mittente: "+ json_response['from']['name'] +
            "\n[*]Oggetto: " + json_response['subject']+
            "\n[*]Data: " + json_response['createdAt']+
            "\n[*]Download link: " + json_response['downloadUrl']+ "\n") 
        
        mail_id = json_response['id']
        return mail_id
   
    
    
        


def main():
    
    # headers = {'Content-Type: application/json'}
    browser = checkParamCL()
    global auth_token
    
    #Genera una stringa casuale di 15 caratteri per l'email e password
    
    address = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))+"@emergentvillage.org"
    password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
    
    # address = "ao13vfntvdbhl1k@emergentvillage.org"	
    # password = "h0eT8QIbRp"
    
    print("\n[######] FASE 1 - GENERAZIONE ACCOUNT EMAIL TEMPORANEA [######]"+"\n")
    print("[INFO] Generazione email: "+address)
    print("[INFO] Generazione password: "+password+"\n")
    

    #crea un account con la mail generata e la password
    
    r = requests.post("https://api.mail.tm/accounts", json={"address": address, "password": password})
    
    json_response = r.json()
    
    account_id = json_response['id']
 
    print ("[INFO] ["+ str(r.status_code)+"] "+"["+r.reason+"] Account creato in data: " + json_response['createdAt'] + " con id: " + json_response['id']+"\n")
    
    


    
    

    print("\n[######] FASE 2 - RIEMPIMENTO FORM WIENER HAUS [######]"+"\n")
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
    email_field_elem.send_keys(address)

    print("[SUCCESS] Valori inseriti!")


    print("[INFO] Ricerca tasto per i coockies")
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

   

    print("[SUCCESS] Controlla la casella postale: ", address, ", divertiti con il tuo 15% di sconto")
    
    
    print("\n[######] FASE 3 - RECUPERO EMAIL CON IL CODICE COUPON  [######]"+"\n")
    
    
    #recupera il token di autenticazione
    r = requests.post("https://api.mail.tm/token", json={"address": address, "password": password})   
    json_response = r.json()
    
    auth_token = json_response['token']
    
    print("[INFO] Token recuperato: "+auth_token[:5] + "..."+ auth_token[20:25] +" per l'account con id: "+json_response['id']+"\n")
    
    #recupera la mail ricevuta
    message_id = checkRecivedEmail()
    
    
    #DEBUG
    print(message_id, type(message_id))
    print(str(message_id), type(str(message_id)))
    
    

    
    r = requests.get("https://api.mail.tm/messages/"+message_id, headers={"Authorization": "Bearer "+auth_token})
    json_response = r.json()
    
    print(json_response, type(json_response))
    
    
    
    
    #Ricarca il link del coupon       
    m = re.search("\[https://wienerhaus\.it/newsletter/confirm\?key=(.+?)]", json_response['text'])
    
    link_coupon = m.group(1)
    
    
    print("[SUCCESS] Chiave del coupon: "+link_coupon+
          "\n[*]Link del coupon: https://wienerhaus.it/newsletter/confirm?key="+link_coupon)
    
    
    
    #apre il browser e va alla pagina del coupon
    openBrowser("https://wienerhaus.it/newsletter/confirm?key="+link_coupon, browser)
    
    browser.find_element(By.XPATH, "/html/body/div[2]/div/a").click()
    
    browser.switch_to.window(browser.window_handles[1])
    
    #recupero imagine coupon
    time.sleep(2)
    
    print("[######] FASE 4 - FINE [######]"+"\n")
    
    print("[INFO] Salvataggio immagine coupon> coupon.png")
    browser.save_full_page_screenshot("coupon.png")
    
    print("[SUCCESS] Coupon salvato!")
    
    print("[INFO] Eliminazione account email temporanea")
    
    r = requests.delete("https://api.mail.tm/accounts/"+account_id, headers={"Authorization": "Bearer "+auth_token})
    
    
    time.sleep(2)
    
    print("\n\n\n\n\n\n....\n....\n...\n..\n.\nBye Bye >:D\n\n\n")

    input("Premi un tasto per chiudere il programma")

    browser.quit()






if __name__ == "__main__":
    main()