from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
import time

FORM_LINK = os.environ["GOOGLE_FORM"]
ZILLOW = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
}

response = requests.get(ZILLOW, headers=headers)
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")
links = soup.find_all(name="a", class_="list-card-link")
links_list = []
for link in links:
    if link['href'].startswith('/b'):
        link['href'] = 'https://zillow.com' + link['href']
        links_list.append(link['href'])
    else:
        links_list.append(link.get("href"))
links_list = list(dict.fromkeys(links_list))
print(links_list)
# print(len(links_list))
prices = soup.find_all(name="div", class_="list-card-price")
prices_list = [price.getText().split("/")[0].split("+")[0].split(" ")[0] for price in prices]
print(prices_list)
# print(len(prices_list))
addresses = soup.find_all(name="address", class_="list-card-addr")
addresses_list = [address.getText().split(" | ")[-1] for address in addresses]
print(addresses_list)
# print(len(addresses_list))

chrome_driver_path = "C:\Development\chromedriver.exe"
drive = webdriver.Chrome(executable_path=chrome_driver_path)


for i in range(len(links_list)):
    drive.get(FORM_LINK)
    time.sleep(2)
    drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(addresses_list[i])
    drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(prices_list[i])
    drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(links_list[i])
    time.sleep(2)
    drive.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span').click()
