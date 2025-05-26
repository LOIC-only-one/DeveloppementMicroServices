import requests

def get_entrypoint(url):
    response = requests.get(url)
    print(f"GET {url} - Status: {response.status_code}")
    data = response.json()
    print(data)
    print('-' * 40)

if __name__ == "__main__":
    base_url = "http://127.0.0.1:80"

    entrypoints = [
        "/get",
        "/ip",
        "/user-agent",
        "/headers",
        "/uuid"
    ]

    for ep in entrypoints:
        get_entrypoint(base_url + ep)