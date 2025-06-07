import requests
import os

def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Archivo {filename} descargado correctamente")

# URL de descarga directa de tu CSV
url = "https://drive.google.com/file/d/1sEcYdeZ5f3JlQwIfn2JtXuD_VaaEiD-7/view?usp=sharing"
download_file(url, "Mision_TIC_2020_100_mil_programadores.csv")