# LAB 03_IDOR

## DOM XSS Attack

1. The initial step involved identifying a user-input vector within the application. The search functionality was identified as a logical candidate for testing.

2. Instead of standard text, a basic XSS payload was injected into the search field: `<iframe src="javascript:alert('xss')">`

3. The execution of the script was confirmed by the appearance of a JavaScript alert window, demonstrating successful script injection and execution in the user's context.
  <img src="./img/1.png" alt="Image 1" style="width:80%; height:auto;">


4. A second, more complex experiment was conducted using an advanced payload designed to manipulate the Document Object Model (DOM): 
```javascript
<iframe src="javascript: document.body.innerHTML // = '<div style=\'font-size:50px;color:white;background:red;padding:40px;text-align:center;\'>XSS DEMO</div>'+ '<p style=\'font-size:30px;text-align:center;\'>This is a demo.</p>'; ">
```
5. This payload successfully overwrote the page content, resulting in the display of a prominent red banner with the text "XSS DEMO," providing a clear visual demonstration of the potential impact of the vulnerability.
<img src="./img/2.png" alt="Image 1" style="width:80%; height:auto;">

## Reflected XSS attack
