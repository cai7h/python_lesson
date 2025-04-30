from bs4 import BeautifulSoup
import csv
from peewee import *

db = MySQLDatabase("1", host="localhost", port=3306, user="root", passwd="3218560376jJ")


# 表结构实体
class Movie(Model):
    title = CharField(max_length=200)
    rating_num = FloatField()
    comment_num = IntegerField()
    directors = CharField(max_length=200)
    actors = CharField(max_length=200)
    year = CharField(max_length=10)
    country = CharField(max_length=100)
    category = CharField(max_length=100)
    pic = CharField(max_length=200)

    class Meta:
        database = db
        table_name = 'douban_movie'


# 读取合并后的文件
with open('douban.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 假设每个页面的内容以特定的分隔符开头，这里以豆瓣页面的 <ol class="grid_view"> 作为分隔依据
page_sections = html.split('<ol class="grid_view">')[1:]


# 保存数据到数据库的函数
def save_data(title, rating_num, comment_num, directors, actors, year, country, category, pic):
    try:
        movie = Movie(
            title=title,
            rating_num=rating_num,
            comment_num=comment_num,
            directors=directors,
            actors=actors,
            year=year,
            country=country,
            category=category,
            pic=pic
        )
        movie.save()
    except Exception as e:
        print(f"保存数据时出错: {e}")


# 创建数据库表
db.create_tables([Movie])

for section in page_sections:
    section = '<ol class="grid_view">' + section
    soup = BeautifulSoup(section, 'lxml')
    movie_list = soup.find('ol', class_='grid_view').find_all('li')
    for movie in movie_list:
        # 电影名称
        title = movie.find('div', class_='hd').find('span', class_='title').get_text()
        # 评价分数
        rating_num = float(movie.find('div', class_='bd').find('div').find('span', class_='rating_num').get_text())
        # 评论人数
        comment_num = int(movie.find('div', class_='bd').find('div').find_all('span')[-1].get_text().strip('人评价'))
        # 导演和主演信息
        directors_info = movie.find('div', class_='bd').find('p').get_text().strip().split('\n')[0].strip()
        directors = directors_info.split('导演: ')[1].split('主演: ')[0].strip()
        if '主演: ' in directors_info:
            actors = directors_info.split('主演: ')[1].strip()
        else:
            actors = ''
        # 上映时间、出品地、剧情类别
        info = movie.find('div', class_='bd').find('p').get_text().strip().split('\n')[1].strip()
        year = info.split('/')[0].strip()
        country = info.split('/')[1].strip()
        category = info.split('/')[2].strip()
        # 电影标题图链接
        pic = movie.find('div', class_='item').find('div', class_='pic').find('a').find('img').get('src')

        # 保存数据到数据库
        save_data(title, rating_num, comment_num, directors, actors, year, country, category, pic)

print('数据抽取并保存到数据库完成。')