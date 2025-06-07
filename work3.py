import os
import pymysql
from bs4 import BeautifulSoup
from peewee import *

# ========== 数据库连接 ==========
pymysql.install_as_MySQLdb()
db = MySQLDatabase(
    database="python_lesson",
    host="localhost",
    port=3306,
    user="root",
    password="Cqh051213",  # 改为你自己的数据库密码
    charset='utf8mb4'
)

# ========== 数据模型 ==========
class DoubanMovie(Model):
    title = CharField(max_length=100)
    rating = FloatField()
    comment_num = IntegerField()
    director = TextField()
    actor = CharField(max_length=100)
    year = IntegerField()
    country = CharField(max_length=50)
    genre = CharField(max_length=100, null=True)
    pic_link = TextField(null=True)

    class Meta:
        database = db
        table_name = 'douban_movie'

# ========== 提取并写入数据库 ==========
def extract_and_store_html_to_db(source_dir):
    count = 0
    for file_name in os.listdir(source_dir):
        if not file_name.endswith(".html"):
            continue  # 跳过非 HTML 文件

        file_path = os.path.join(source_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")
        movie_items = soup.select("ol.grid_view li")  # 获取电影项列表

        for idx, movie in enumerate(movie_items, 1):
            try:
                # 标题
                title_tag = movie.find("span", class_="title")
                title = title_tag.get_text(strip=True) if title_tag else "无标题"

                # 评分
                rating_tag = movie.find("span", class_="rating_num")
                rating = float(rating_tag.get_text(strip=True)) if rating_tag else 0.0

                # 评论人数
                star_div = movie.find("div", class_="star")
                comment_text = star_div.find_all("span")[-1].get_text(strip=True) if star_div else ""
                comment_num = int(''.join(filter(str.isdigit, comment_text))) if comment_text else 0

                # 导演与主演
                p_tag = movie.find("div", class_="bd").find("p")
                info_text = p_tag.get_text(strip=True) if p_tag else ""
                director, actor = "", ""
                if "导演" in info_text:
                    parts = info_text.split("主演:")
                    director = parts[0].replace("导演:", "").strip()
                    actor = parts[1].strip() if len(parts) > 1 else ""

                # 年份 / 国家 / 类型（新版解析方式，兼容多种换行结构）
                year = 0
                country = ""
                genre = ""
                detail_line = ""
                if p_tag:
                    for line in p_tag.stripped_strings:
                        if '/' in line and any(c.isdigit() for c in line):
                            detail_line = line
                            break
                parts = [p.strip() for p in detail_line.split('/')]
                if len(parts) > 0 and parts[0][:4].isdigit():
                    year = int(parts[0][:4])
                country = parts[1] if len(parts) > 1 else ""
                genre = parts[2] if len(parts) > 2 else ""

                # 图片链接
                pic_tag = movie.find("img")
                pic_link = pic_tag.get("src") if pic_tag else ""

                # 写入数据库
                DoubanMovie.create(
                    title=title,
                    rating=rating,
                    comment_num=comment_num,
                    director=director,
                    actor=actor,
                    year=year,
                    country=country,
                    genre=genre,
                    pic_link=pic_link
                )
                print(f"[成功] 第{count + 1}部：{title}")
                count += 1

            except Exception as e:
                print(f"[跳过] {file_name} 第{idx}条写入失败：{e}")

    print(f"\n✅ 共写入 {count} 部电影信息")

# ========== 主程序入口 ==========
if __name__ == "__main__":
    db.connect()
    db.drop_tables([DoubanMovie])                # 重新创建表（谨慎使用，会清空数据）
    db.create_tables([DoubanMovie])
    db.execute_sql("ALTER TABLE douban_movie AUTO_INCREMENT = 1;")  # id 从1开始

    # 修改为目标路径（使用原始字符串避免反斜杠转义）
    html_source_dir = r"C:\Users\CK\Desktop\inventory"
    extract_and_store_html_to_db(html_source_dir)