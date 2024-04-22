import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def scrape_page(url):
    # Send a GET request to the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <a> tags
        all_links = soup.find_all("a")

        # Filter links that start with /torrent
        torrent_links = [
            link.get("href")
            for link in all_links
            if link.get("href") and link.get("href").startswith("/torrent")
        ]

        # Convert relative URLs to absolute URLs
        base_url = "https://1337x.to"  # Base URL of the website
        torrent_links = [urljoin(base_url, link) for link in torrent_links]

        magnet_links = []
        # Download torrent files
        for link in torrent_links:
            # Send a GET request to the link
            link_response = requests.get(link)

            # Check if the request was successful
            if link_response.status_code == 200:
                # Parse the HTML content of the link response
                link_soup = BeautifulSoup(link_response.content, "html.parser")

                # Find all <a> tags
                all_links = link_soup.find_all("a")

                # Find all <a> tags with href starting with "magnet:"

                for link in all_links:
                    try:
                        if link.get("href") and link.get("href").startswith("magnet:"):
                            magnet_links.append(link["href"])
                    except Exception:
                        continue
                print("...")
            else:
                print(f"Failed to retrieve torrent file from {link}")
        return list(set(magnet_links))
    else:
        print("Failed to retrieve webpage.")


# Check if command-line argument is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <argument>")
    sys.exit(1)

# Get the command-line argument
base_url = sys.argv[1]

# Base URL of the website
print("Base URL:", base_url)

all_magnet_links = []
page_number = 1
while True:
    page_url = f"{base_url}/{page_number}/"
    magnet_links = scrape_page(page_url)
    if not magnet_links:
        break
    all_magnet_links.extend(magnet_links)
    print(f"Page Number: {page_number} | Done.")
    page_number += 1

# Write magnet links to a text file
file = open("magnet_links.txt", "w")
for magnet_link in all_magnet_links:
    file.write(magnet_link + "\n")
file.close()

print("Magnet links added to 'magnet_links.txt' file.")
