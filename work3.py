from bs4 import BeautifulSoup
from peewee import *
import re

# 数据库连接配置
db = MySQLDatabase(
    "python_lesson",
    host="localhost",
    port=3306,
    user="root",
    password="Cqh051213"  # 注意：实际项目中应使用更安全的密码存储方式
)


class Movie(Model):
    """豆瓣电影数据模型"""
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


def parse_movie_info(movie_element):
    """解析单个电影元素，提取电影信息"""
    try:
        # 电影名称
        title = movie_element.find('div', class_='hd').find('span', class_='title').get_text(strip=True)
        
        # 评价分数
        rating_num = float(movie_element.find('div', class_='bd').find('div').find('span', class_='rating_num').get_text())
        
        # 评论人数
        comment_text = movie_element.find('div', class_='bd').find('div').find_all('span')[-1].get_text(strip=True)
        comment_num = int(re.search(r'(\d+)', comment_text).group(1))
        
        # 导演和主演信息
        info_paragraph = movie_element.find('div', class_='bd').find('p').get_text(strip=True)
        lines = info_paragraph.split('\n')
        directors_info = lines[0].strip()
        
        directors_match = re.search(r'导演:\s*(.*?)(?:\s*主演:|$)', directors_info)
        directors = directors_match.group(1).strip() if directors_match else ''
        
        actors_match = re.search(r'主演:\s*(.*)', directors_info)
        actors = actors_match.group(1).strip() if actors_match else ''
        
        # 上映时间、出品地、剧情类别
        if len(lines) > 1:
            info_line = lines[1].strip()
            parts = info_line.split('/')
            year = parts[0].strip() if parts else ''
            country = parts[1].strip() if len(parts) > 1 else ''
            category = parts[2].strip() if len(parts) > 2 else ''
        else:
            year = country = category = ''
        
        # 电影标题图链接
        pic = movie_element.find('div', class_='item').find('div', class_='pic').find('a').find('img').get('src', '')
        
        return {
            'title': title,
            'rating_num': rating_num,
            'comment_num': comment_num,
            'directors': directors,
            'actors': actors,
            'year': year,
            'country': country,
            'category': category,
            'pic': pic
        }
    except (AttributeError, ValueError, IndexError) as error:
        print(f"解析电影信息时出错: {error}")
        return None


def save_movie(data):
    """保存电影数据到数据库"""
    if not data:
        return
    
    try:
        with db.atomic():
            Movie.create(**data)
    except IntegrityError as error:
        print(f"数据完整性错误: {error}")
    except Exception as error:
        print(f"保存数据时出错: {error}")


def main():
    """主函数：读取HTML文件，解析数据并保存到数据库"""
    try:
        # 连接数据库
        db.connect()
        # 创建数据表
        db.create_tables([Movie])
        
        # 读取HTML文件
        with open('douban.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # 分割页面内容
        page_sections = html_content.split('<ol class="grid_view">')[1:]
        
        # 解析并保存每部电影信息
        for section in page_sections:
            section = '<ol class="grid_view">' + section
            soup = BeautifulSoup(section, 'lxml')
            movie_list = soup.find('ol', class_='grid_view').find_all('li')
            
            for movie in movie_list:
                movie_data = parse_movie_info(movie)
                save_movie(movie_data)
        
        print('数据抽取并保存到数据库完成。')
    except FileNotFoundError:
        print("错误：找不到douban.html文件")
    except Exception as error:
        print(f"发生未知错误: {error}")
    finally:
        # 关闭数据库连接
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()    