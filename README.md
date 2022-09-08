

# 🎟 Wiener Haus Coupon Generator

![](https://github.com/habby1337/WH-Restourant-Coupon-Generator/blob/main/images/logo_200x200.png?raw=true)

![](https://img.shields.io/github/issues/habby1337/WH-Restourant-Coupon-Generator) ![](https://img.shields.io/github/forks/habby1337/WH-Restourant-Coupon-Generator) ![](https://img.shields.io/github/stars/habby1337/WH-Restourant-Coupon-Generator)  ![](https://img.shields.io/github/license/habby1337/WH-Restourant-Coupon-Generator) 
![](https://img.shields.io/badge/Release-Windows%20Ready-brightgreen)




# ⭐ Features

- Generazione automatica accout email temporaneo
- Compilazione form di WH
- Eliminazione automatica dell'account email 
- Download automatico del coupon
- Invio diretto su telegram del coupom


# ❓ Come installare
## 🤷🏻‍♂️ Cosa scaricare

1. Scaricare l'ultima versione di [WH Coupon Generator](https://github.com/habby1337/WH-Restourant-Coupon-Generator/releases)
2. Installare **Python** con una versione: *< 3.10.4*
3. Scaricare i webdriver per Selenium
	- Chrome (chromedriver) > [Clicca qui](https://chromedriver.chromium.org/downloads)
	- Firefox (geckodriver) > [Clicca qui](https://github.com/mozilla/geckodriver/releases/)
4. Recuperare la chiave per il bot di telegram > [Telegram Docs](https://core.telegram.org/bots#6-botfather)
5. Recupearare la propria chat id di telegram > [Telegram Chat with MyIdBot](https://t.me/myidbot)

___

### 🛠 Configurare il file Config.py
Aprire il file e inserire i seguenti valori:
- Token API Bot Telegram:
`telelgram_bot_api_key = "<yourTelegramBotApiKey>"`
- Chat id di Telegram
`telegram_chat_id = "<yourTelegramChatID>"`
- Proxy Setting
    questi impostati sono i valori che funzionano meglio (default)
    ```
    ProxySettings["last_check"] = "9800" // Ultimo check avvenuto
    ProxySettings["uptime"] = "20" // Da quanto tempo risulta online il server 
    ProxySettings["ping"] = "90" // Il suo ping medio
    ProxySettings["country"] = "it,fr,de,al,uk,ru,ro,pl,se,mt,md,me,fn,ag,yt,us,br,jp,mx,co,bg,gb,nl,by,es,at" // Da quale paese proviene il server
    ```

    - ProxySettings["last_check"]:
      - Valore più basso: valori aggioranti più recentemente
    - ProxySettings["uptime"]:
      - Valore più alto: Server più stabile
    - ProxySettings["ping"]:
      - Valore più basso: Server più performante 
    - ProxySettings["country"]:
      - Lista dei paesi in cui viene recuperato il server, puoi vedere la lista da [qui](https://www.proxyscan.io/api)


Puoi vedere tutti i valori dalla pagina delle API, [clicca qui](https://www.proxyscan.io/api)

___

### 🧾 Installare Requisiti
Per installare i requisiti eseguire il comando: 
```
$cd /path/to/WH-Restourant-Coupon-Generator
$pip install -r requirements.txt
```

___

#### 🔥 Come avviare
Per avviare il generatore eseguire si posso usare i seguenti modi

- **Tramite Command Line:**
`
$python WH_Coupon_generator.py <browser type>
`


- **Tramite Bat Script**
`
$echo start cmd /k python /path/to/WH_Coupon_generator.py 1 > Starter_Script.bat
`

___

## ⚙ Valori per Command line

| Browser Name | Value |
| ------------ | ----- |
| Firefox      | 1     |
| Chrome       | 2     |

Da utilizzare nel seguente modo:

`$python WH_Coupon_generator.py <value>`


___


# 🆕 Aggiornamenti futuri in programma

- [x] Inviare coupon tramite chat telegram
- [x] Verificare il funzionamento dei proxy prima dell' utilizzo
- [x] Eliminazione vecchi file coupon e log
- [x] Time stamp delle operazioni
- [x] Generazione logs
- [ ] Migliormaneto attributi inseriti nella comand line 
    - [ ] Valore del browser
    - [ ] Telegram token
    - [ ] Chat id per il messaggio su telegram
- [ ] Ottimizzare l'esecuzione
- [ ] GUI
- [ ] Spostare le funzioni in file separati per migliorare la leggibilià del codice


___

# 🩹 BUG noti in corso di patch

- Possibilità di utilizzare un solo browser (Firefox)
- I valori passati tramite CL non funzionano 