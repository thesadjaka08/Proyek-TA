import requests

url = "https://developers.google.com/gmail/markup/reference/formats/json-ld"

response = requests.get(url)

if response.status_code == 200:
    with open("json-ld.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Konten berhasil didownload dan disimpan sebagai json-ld.html")
else:
    print(f"Gagal mendownload konten. Status code: {response.status_code}")
