#encoding utf-8
import csv
import re
from bs4 import BeautifulSoup as soup
import urllib.request
from selenium import webdriver

# adding incognito
link='https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=9EX8GBHW49QAPREDWBWC&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2'
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
driver = webdriver.Chrome(executable_path='/Users/aayushsharma/python/voterlist/chromedriver', chrome_options=option)

driver.get(link)
page_html = driver.page_source
page_soup = soup(page_html, 'lxml')
# print(page_soup)
table = page_soup.find('tbody')
# print(table)
rows= table.find_all('tr')
writer_list=[]
for row in rows:
    writerx = {}
    genre = []
    cast=[]
    reviews=[]
    name_div = row.find("td",{"class":"titleColumn"})
    name_a = name_div.find('a',href=True)
    name = name_a['href']
    driver.get('https://www.imdb.com'+name)
    single_page = driver.page_source
    single_soup = soup(single_page,'lxml')
    title_wrapper = single_soup.find('div',{'class':'title_wrapper'})
    if single_soup.find('div', {'class': 'ratings_wrapper'}):
        ratings_wrapper = single_soup.find('div', {'class': 'ratings_wrapper'})
        rating = ratings_wrapper.find('span', {'itemprop': 'ratingValue'}).text
    else:
        rating = "N/A"

    subtext_div =single_soup.find('div', {'class': 'subtext'})
    name_div = title_wrapper.find('h1',{'itemprop':'name'})
    name = name_div.text
    year = name_div.find('span',{'id':'titleYear'}).text
    if subtext_div.find('meta',{'itemprop':'contentRating'},content=True):
        content_rating_div = subtext_div.find('meta',{'itemprop':'contentRating'},content=True)
        content_rating = content_rating_div['content']
    else:
        content_rating="N/A"
    if subtext_div.find('time',{'itemprop':'duration'}):
        time = subtext_div.find('time',{'itemprop':'duration'}).text.strip()
    else:
        time="N/A"
    genres = subtext_div.find_all('a')
    synopsis=single_soup.find('div', {'class': 'summary_text'}).text.strip()
    director_div =single_soup.find('span', {'itemprop': 'director'})
    director = director_div.find('span', {'class': 'itemprop'}).text.strip()
    writer_div = single_soup.find('span', {'itemprop': 'creator'})
    writer = writer_div.find('span', {'class': 'itemprop'}).text.strip()
    cast_div =single_soup.find_all('span', {'itemprop': 'actors'})
    if single_soup.find('div', {'class': 'user-comments'}):
        review_div =single_soup.find('div', {'class': 'user-comments'})
        review_links = review_div.find_all('a',href=True)
        review_link =review_links[-1]['href']
    else:
        review_link = "N/A"
        reviews.append("N/A")
    for casts1 in cast_div:
        cast.append(casts1.text.strip())
    for genres1 in genres[:-1]:
        genre.append(genres1.text.strip())
    writerx["name"] = name
    if single_soup.find("div", {"class": "poster"}):
        posterdiv = single_soup.find("div", {"class": "poster"})
        img = posterdiv.find("img", src=True)
        image_link = (img["src"])
        urllib.request.urlretrieve(image_link, "posters/x/" + name.split(" ")[0] + ".jpg")
    else:
        name="N/A"
    # print("Movie Name:"+name)
    # print("Movie Year:"+year)
    # print("Movie Rating:"+rating)
    # print("Movie Time:"+time)
    # print("Movie Genre:"+str(genre))
    # print("Content Rating:"+content_rating)
    # print("Movie Synopsis:"+synopsis)
    # print("Movie Director:"+director)
    # print("Movie Writer:"+writer)
    # print("Movie Cast:"+str(cast))
    if len(review_link)>5:
        driver.get('https://www.imdb.com'+review_link)
        review_page = driver.page_source
        review_soup = soup(review_page, 'lxml')
        review_div =review_soup.find('div',{'class':'lister-list'})
        review_div2 = review_soup.find_all('div', {'class': 'text show-more__control'})
        for reviewsx in review_div2:
            reviews.append(reviewsx.text.strip())

    # print("Movie Reviews"+ str(reviews))

    writerx["year"] =year.replace("-","")
    writerx["rating"] =rating
    writerx["duration"] =time
    writerx["genre"] =genre
    writerx["content_rating"] =content_rating
    writerx["synopsis"] =synopsis
    writerx["director"] =director
    writerx["writer"] =writer
    writerx["cast"] =cast
    writerx["reviews"] = reviews
    writerx["poster"] = "/posters/x"+name.split(" ")[0] + ".jpg"
    writer_list.append(writerx.copy())
print(writer_list)
with open('movies.csv','w') as newfile:
    writingdict=csv.DictWriter(newfile,fieldnames=["name","year","rating","duration","genre","content_rating",
                                                       "synopsis","director","writer","cast","reviews","poster"])
    writingdict.writeheader()
    writingdict.writerows(writer_list)






