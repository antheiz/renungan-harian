import requests
from bs4 import BeautifulSoup

# URL dari halaman yang akan di-scrape
url = "https://alkitab.app/renunganpagi/"

# Mengirimkan request HTTP ke halaman
response = requests.get(url)

# Memastikan request berhasil
if response.status_code == 200:
    # Parsing HTML dari halaman
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Mengambil judul dari halaman
    title_element = soup.find('big')
    if title_element:
        title = title_element.text.strip()
        for link in title_element.find_all('a', href=True):
            clean_href = link['href'].replace(' ', '%20')
            link_text = f"[{link.text}]({clean_href})"
            title = title.replace(link.text, link_text)
    else:
        title = "Judul tidak ditemukan"
    
    # Mengambil waktu dari halaman
    time_element = soup.find('div', class_='me-date')
    time = time_element.text.strip() if time_element else "Waktu tidak ditemukan"
    
    # Mengambil gambar header dari halaman
    container = soup.find('div', class_='me-container')
    header_img_element = container.find('img') if container else None
    header_img_url = "https://alkitab.app" + header_img_element['src'] if header_img_element else "Gambar header tidak ditemukan"
    
    # Mengambil konten dan link href dari halaman
    content_elements = soup.find_all('p', class_='me-content')
    content = ""
    for element in content_elements:
        paragraph = element.text.strip()
        for link in element.find_all('a', href=True):
            clean_href = link['href'].replace(' ', '%20')
            link_text = f"[{link.text}]({clean_href})"
            paragraph = paragraph.replace(link.text, link_text)
        content += paragraph + "\n\n"

    content = content.strip() if content else "Konten tidak ditemukan"
    
    # Menampilkan hasil dalam format Markdown
    markdown_output = f"""
# {title}

![Header Image]({header_img_url})

> {time}

{content}
    """
    # Update README.md
    with open("README.md", "w") as f:
        f.write(markdown_output)
else:
    print("Halaman tidak dapat diakses")
