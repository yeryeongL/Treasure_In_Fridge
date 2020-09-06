import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.myproject

#재료 가져오기
# DB에 저장할 레시피의 url을 가져옵니다.


def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data=''
    for i in range(1,20):
            source='https://www.10000recipe.com/recipe/list.html?order=reco&page='+str(i)
            response=requests.get(source)
            data=data+response.text
            soup = BeautifulSoup(data, 'html.parser')

            lis = soup.select('#contents_area_full > ul > ul > li')

            urls = []

            for li in lis:
                a = li.select_one('div.common_sp_thumb > a')
                if a is not None:
                    base_url = 'https://www.10000recipe.com/'
                    url = base_url + a['href']
                    urls.append(url)

                    # print(urls)

    return urls

def insert_recipe(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    name = soup.select_one('#contents_area > div.view2_summary > h3').text
    img_url =soup.select_one('#main_thumbs')['src']

    ingredients=[]

    rec=soup.find('div','ready_ingre3')

    try:
        for i in rec.find_all('ul'):


            for tmp in i.find_all('li'):
                tmp.span.decompose()  #하위태그 삭제했음
                ingredient=tmp.get_text().replace('\n','').replace(' ','')
                ingredients.append(ingredient)

            # ingredients.append(recipe)
    except(AttributeError):
        return




    doc={
        'name': name,
        'img_url': img_url,
        'ingredients': ingredients,
        'url': url

    }

    print('완료!',ingredients)

    db.recipe.insert_one(doc)

def insert_all():
    db.recipe.drop()
    urls = get_urls()
    for url in urls:
        insert_recipe(url)


insert_all()
