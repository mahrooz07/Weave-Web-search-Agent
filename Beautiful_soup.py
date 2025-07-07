# from bs4 import BeautifulSoup
# import requests

# url = "https://www.geeksforgeeks.org/cpp-tutorial/"
# response = requests.get(url)

# soup = BeautifulSoup(response.content)
# print(soup.prettify())

from bs4 import BeautifulSoup
import requests

# Send GET request to fetch the webpage
url = "https://www.geeksforgeeks.org/cpp-tutorial/"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract text from all paragraph tags
paragraphs = soup.find_all('p')

# Clean and print the text from each paragraph
for paragraph in paragraphs:
    # Get the text inside the <p> tag and print it
    print(paragraph.get_text())
    print("\n")  # Adds a newline for better readability between paragraphs
