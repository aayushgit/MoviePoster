import csv
import re
from bs4 import BeautifulSoup as soup
import urllib.request
from selenium import webdriver
movielist=[]
with open("movie_metadata.csv") as data:
    readCSV=csv.reader(data,delimiter=",")
    for row in readCSV:
        movielist.append(row[17])

imdblink=movielist[1:]
# print(imdblink)
# adding incognito
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
i=0
for link in imdblink:
    i=i+1
    # opening an instance of browser
    driver = webdriver.Chrome(executable_path='/Users/aayushsharma/python/voterlist/chromedriver', chrome_options=option)
    driver.get(link)
    x=str(link)
    page_html = driver.page_source
    page_soup = soup(page_html, 'lxml')
    posterdiv = page_soup.find("div", {"class": "poster"})
    img = posterdiv.find("img",src=True)
    image_link=(img["src"])
    urllib.request.urlretrieve(image_link, "posters/"+str(i)+".jpg")


