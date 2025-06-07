import os
from bs4 import BeautifulSoup

# 设置新的 HTML 文件夹路径和输出 TXT 文件路径
source_dir = r"C:\Users\CK\Desktop\inventory"  # 修改为目标目录
output_file = os.path.join(source_dir, "douban_extracted.txt")  # 输出文件仍放在该目录下

# 检查源目录是否存在，不存在则创建（避免文件读取错误）
if not os.path.exists(source_dir):
    os.makedirs(source_dir)
    print(f"提示：源目录 {source_dir} 不存在，已自动创建")

# 打开输出文件用于写入
with open(output_file, "w", encoding="utf-8") as out:
    # 遍历源目录下的所有文件
    for file_name in os.listdir(source_dir):
        # 只处理 HTML 文件
        if not file_name.endswith(".html"):
            continue

        # 构造完整的 HTML 文件路径
        file_path = os.path.join(source_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, "lxml")
        movie_items = soup.select("ol.grid_view li")  # 获取电影项列表

        # 遍历每部电影的信息
        for movie in movie_items:
            try:
                # 标题（主标题）
                title_tag = movie.find("span", class_="title")
                if not title_tag:
                    print(f"[跳过] 未找到标题：{file_name}")
                    continue
                title = title_tag.get_text(strip=True)

                # 评分
                rating_tag = movie.find("span", class_="rating_num")
                rating = rating_tag.get_text(strip=True) if rating_tag else ""

                # 评论人数（从星标区域提取）
                star_div = movie.find("div", class_="star")
                comment_text = star_div.find_all("span")[-1].get_text(strip=True) if star_div else ""
                comment_num = ''.join(filter(str.isdigit, comment_text))  # 提取纯数字

                # 导演与主演（从简介段落提取）
                p_tag = movie.find("div", class_="bd").find("p")
                info_text = p_tag.get_text(strip=True) if p_tag else ""
                director, actor = "", ""
                if "导演" in info_text:
                    parts = info_text.split("主演:")
                    director = parts[0].replace("导演:", "").strip()  # 导演信息
                    if len(parts) > 1:
                        actor = parts[1].strip()  # 主演信息（可能为空）

                # 年份 / 国家 / 类型（从简介段落的第二行提取）
                lines = p_tag.get_text().split("\n") if p_tag else []
                last_line = lines[-1].strip() if len(lines) > 1 else ""
                detail_parts = last_line.split("/")
                year = detail_parts[0].strip() if len(detail_parts) > 0 else ""  # 年份
                country = detail_parts[1].strip() if len(detail_parts) > 1 else ""  # 国家
                genre = detail_parts[2].strip() if len(detail_parts) > 2 else ""  # 类型

                # 海报图片链接
                img_tag = movie.find("img")
                pic_link = img_tag.get("src") if img_tag else ""

                # 写入 TXT 文件（使用制表符 \t 分隔字段，方便后续处理）
                out.write(f"{title}\t{rating}\t{comment_num}\t{director}\t{actor}\t{year}\t{country}\t{genre}\t{pic_link}\n")
                print(f"[成功] 写入：{title}")

            except Exception as e:
                print(f"[跳过] 某部电影解析失败：{e}")