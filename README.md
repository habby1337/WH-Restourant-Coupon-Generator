

# 🎟 Wiener Haus Coupon Generator

![](https://github.com/habby1337/WH-Restourant-Coupon-Generator/blob/main/images/logo_200x200.png?raw=true)

![](https://img.shields.io/github/issues/habby1337/WH-Restourant-Coupon-Generator) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg)  ![](https://img.shields.io/bower/v/editor.md.svg)




# ⭐ Features

- Generazione automatica accout email temporaneo
- Compilazione form di WH
- Eliminazione automatica dell'account email 
- Download automatico del coupon
- Invio diretto su telegram del coupom


# ❓ Come installare
## 🤷🏻‍♂️ Cosa scaricare

1. Installare **Python** con una versione: *< 3.10.4*
2. Scaricare i webdriver per Selenium
	- Chrome (chromedriver) > [Clicca qui](https://chromedriver.chromium.org/downloads)
	- Firefox (geckodriver) > [Clicca qui](https://github.com/mozilla/geckodriver/releases/)
3. Recuperare la chiave per il bot di telegram > [Telegram Docs](https://core.telegram.org/bots#6-botfather)
4. Recupearare la propria chat id di telegram > [Telegram Chat with MyIdBot](https://t.me/myidbot)

### 🧾 Installare Requisiti
Per installare i requisiti eseguire il comando: 
```
$cd /path/to/WH-Restourant-Coupon-Generator
$pip install -r requirements.txt
```
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

### 📁 File eliminabili non necessari
Lista dei file e cartelle eliminabili.
- Images/
- STARTERS/
- .gitattributes
- .gitignore
- LICENSE
- README.md

___

## ⚙ Valori per Command line

| Browser Name | Value |
| ------------ | ----- |
| Firefox      | 1     |
| Chrome       | 2     |

Da utilizzare nel seguente modo:

`$python WH_Coupon_generator.py <value>`



___
# 🆕 Aggiornamenti programmati

- [x] Inviare coupon tramite chat telegram
- [x] Verificare il funzionamento dei proxy prima dell' utilizzo
- [x] Eliminazione vecchi file coupon e log
- [x] Time stamp delle operazioni
- [ ] Migliormaneto attributi inseriti nella comand line 
    - [ ] Valore del browser
    - [ ] Telegram token
    - [ ] Chat id per il messaggio su telegram
- [ ] Ottimizzare l'esecuzione
- [ ] Generazione logs

