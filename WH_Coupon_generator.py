from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time





def openBrowser(url, browser):
    """Apertura browser su paramentro url

    Args:
        url (string): Url del sitoweb da visitare

    Returns:
        object: Ritorno dell' oggetto browser 
    """
    
    print("[INFO] Apertura browser su url\"",url,"\"...")
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
    browser = checkParamCL()
    
    
    #apertura browser su sito web mail 
    openBrowser("https://mail.tm/it/", browser)
    
    
    #Chiusura dialgo coockies
    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[3]").click()

    time.sleep(2)
    #recupero mail 
    #copia indirizzo mail
    email = browser.find_element(By.ID, "DontUseWEBuseAPI").text()
    
   


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