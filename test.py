from bs4 import BeautifulSoup
import httpx

request = httpx.get('https://bank.uz/uz/currency')
soup = BeautifulSoup(request.content, 'html.parser')

aria_controls_values = [a['aria-controls'] for a in soup.find_all('a') if 'aria-controls' in a.attrs]

# Extracting text from elements with class "medium-text"
medium_text_values = [element.text.strip() for element in soup.find_all('tabs-a', 'span', class_='medium-text')]

print(aria_controls_values)
print(medium_text_values)
