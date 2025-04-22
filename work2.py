import os
from bs4 import BeautifulSoup

dest_dir = "d:/Github/python_lesson/"

for html_file in os.listdir(dest_dir):
    full_path = os.path.join(dest_dir, html_file)
    if os.path.isfile(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                html = f.read()
                soup = BeautifulSoup(html, 'lxml')
                movie_list = soup.find('ol', class_='grid_view')
                if movie_list:
                    for movie in movie_list.find_all('li'):
                        title_element = movie.find('div', class_='hd')
                        if title_element:
                            title = title_element.find('span', class_='title')
                            title = title.get_text(strip=True) if title else "No title found"
                        else:
                            title = "No title element found"
                        rating_num = movie.find('span', class_='rating_num')
                        rating_num = rating_num.get_text(strip=True) if rating_num else "No rating found"
                        comment_span = movie.find('div', class_='star').find_all('span') if movie.find('div', class_='star') else []
                        comment_num = comment_span[-1].get_text(strip=True) if comment_span and len(comment_span) > 0 else "No comments found"
                        directors = movie.find('div', class_='bd').find('p').get_text(strip=True) if movie.find('div', class_='bd') else "No directors found"
                        link_element = movie.find('div', class_='pic').find('a') if movie.find('div', class_='pic') else None
                        link = link_element.get('href') if link_element else "No link found"
                        pic_element = movie.find('div', class_='pic').find('img') if movie.find('div', class_='pic') else None
                        pic = pic_element.get('src') if pic_element else "No picture found"
                        print(title, rating_num, comment_num, directors, link, pic)
                else:
                    print(f"No movie list found in {html_file}")
        except PermissionError:
            print(f"Permission denied for {full_path}")
        except Exception as e:
            print(f"An error occurred while processing {html_file}: {e}")
    else:
        print(f"Skipping directory: {html_file}")