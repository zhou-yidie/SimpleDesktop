import os
import urllib.request
import urllib.error

# Ensure target directory exists
target_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\literature"
os.makedirs(target_dir, exist_ok=True)

# List of papers/documents to download (Title, URL)
papers = [
    ("Modern Operating Systems 4th Edition.pdf", 
     "https://github.com/lighthousand/books/raw/master/Modern%20Operating%20Systems%204th%20Edition--Andrew%20Tanenbaum.pdf"),
]

# Alternate links for Clean Architecture to try sequentially
clean_architecture_urls = [
    "https://github.com/vslopes/Clean-Code/raw/master/Clean%20Architecture%20-%20Robert%20C.%20Martin.pdf",
    "https://github.com/maksim77/books/raw/master/Clean%20Architecture%20-%20Robert%20C.%20Martin.pdf",
    "https://github.com/guzmanra/books/raw/master/Clean%20Architecture%20-%20Robert%20C.%20Martin.pdf",
    "https://github.com/read-books/Clean-Architecture/raw/master/Clean-Architecture.pdf",
]

# Configure headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Download standard documents
for title, url in papers:
    dst_path = os.path.join(target_dir, title)
    if os.path.exists(dst_path):
        print(f"Skipping (already exists): {title}")
        continue
    print(f"Downloading: {title} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=400) as response:
            with open(dst_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded: {title}")
    except Exception as e:
        print(f"Failed to download {title}: {e}")

# Download Clean Architecture
clean_arch_dst = os.path.join(target_dir, "Clean Architecture.pdf")
if not os.path.exists(clean_arch_dst):
    downloaded = False
    for url in clean_architecture_urls:
        print(f"Trying Clean Architecture from: {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as response:
                with open(clean_arch_dst, 'wb') as out_file:
                    out_file.write(response.read())
            print("Successfully downloaded: Clean Architecture.pdf")
            downloaded = True
            break
        except Exception as e:
            print(f"Failed from this mirror: {e}")
    if not downloaded:
        print("Could not download Clean Architecture.pdf from current mirrors.")
else:
    print("Skipping (already exists): Clean Architecture.pdf")
