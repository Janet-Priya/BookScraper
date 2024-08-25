#Just a guide for the code

#importing all the modules
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

#using the books to scrape site cos neat layout ig
scrapee=requests.get("https://books.toscrape.com")
soup=BeautifulSoup(scrapee.content,'html.parser')
categories=soup.findAll('a')

#scraping all the genres from the site
cats=[]
for link in categories:
  href=link.get('href')
  if href:
    match = re.search(r'category/books/([a-zA-Z]+)_\d+', href)
    if match:
      genre=match.group(1)
      cats.append(genre)

#yay! The program starts!
print('Welcome to the BookScraper!')
sleep(3)

#idek why i included this useless info
instock=soup.findAll('i',attrs={'class':'icon-ok'})
print('The number of books that are in stock are:',len(instock)*50)
print('That\'s a lot of books!')
sleep(3)

#prints it one below the other
print('Now let\'s see what books you prefer!')
print('Choose your genre accordingly: ')
for i in range(len(cats)):
  sleep(0.01)
  y=(cats[i])
  print(y)

sleep(0.5)
genre=input('Choose!: ')
genre=genre.lower()
if genre not in (cats):
  print('Kindly choose from the list.')
else:
  print('Okay,you have chosen',genre)
  for link in categories:#since all the genre links have the similiar layout this is used lol
    href=link.get('href')
    if href and genre in href:
      match=re.search(r'category/books/([a-zA-Z]+)_(\d+)',href)
      if match:
        category_number=match.group(2)
        break

#that genre becomes the link for the user for now
gen_url = f'https://books.toscrape.com/catalogue/category/books/{genre}_{category_number}/index.html'
gen = requests.get(gen_url)
soup = BeautifulSoup(gen.text, 'html.parser')
sleep(2)
results=soup.findAll('strong')
if results:
  results=results[1].text
  results=int(results)
  print('The number of book(s) in that genre are',results)


print('The book(s) are: ')
print()
bks = soup.findAll('a', attrs={'title': True})
l = [bk['title'] for bk in bks] 

for index, title in enumerate(l, start=1):
    sleep(0.5) 
    print(f"{index}. {title}")

while True:
  num = int(input('Choose the number from the books: '))
  if 1 <= num <= len(l):
      tit=l[num - 1]
      print('You have chosen:', tit)
      break
  else:
      print("Invalid choice. Please choose a number from the list.")

#the preferred book page is not shown in the UI
chrome_options=Options()
chrome_options.add_argument("--headless")

#creates a new url and driver
path = r"C:\Users\janet\Downloads\chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get(gen_url)

#here it waits for the site to load and then goes to the page where the chosen book info is there
try:
  
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//a[@title='{tit}']")))
    element.click()
    driver.switch_to.window(driver.window_handles[-1])
    while True:
      print('What do you want to know about the book?')
      w = input('Cost, Star-Rating, Description, UPC or E(Exit): ').lower()
      book_page = BeautifulSoup(driver.page_source, 'html.parser')
      if w == 'cost':
        cost = book_page.find('p', attrs={'class': 'price_color'}).text
        print(f"Cost: {cost}")
      elif w == 'star-rating' or w == 'star-rating':
        rating = book_page.find('p', class_='star-rating')['class'][1]
        print(f"Star Rating: {rating}")
      elif w == 'description':
        description = book_page.find('meta', attrs={'name': 'description'})['content'].strip()
        print(f"Description: {description}")
      elif w == 'upc':
        upc = book_page.find('th', text='UPC').find_next_sibling('td').text
        print(f"UPC: {upc}")
      elif w=='e' or w=='exit':
        print('Thank you for using my BookScraper')
        break
      else:
        print("Invalid choice.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
        


















    

