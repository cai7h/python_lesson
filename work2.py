"""
A script to extract movie information from HTML files.

This script reads HTML files from a specified directory, parses them using BeautifulSoup,
and extracts movie-related information including title, rating, comment count, directors, link, and picture URL.
"""

import os
from bs4 import BeautifulSoup

DESTINATION_DIRECTORY = "d:/Github/python_lesson/"


def extract_movie_info(movie_element):
    """
    Extracts detailed information from a movie element.

    Args:
        movie_element (bs4.element.Tag): A BeautifulSoup Tag representing a movie element.

    Returns:
        tuple: A tuple containing extracted movie information.
    """
    title_element = movie_element.find('div', class_='hd')
    title = title_element.find('span', class_='title').get_text(strip=True) \
        if title_element and title_element.find('span', class_='title') else "No title found"

    rating_num = movie_element.find('span', class_='rating_num').get_text(strip=True) \
        if movie_element.find('span', class_='rating_num') else "No rating found"

    comment_span = movie_element.find('div', class_='star').find_all('span') \
        if movie_element.find('div', class_='star') else []
    comment_num = comment_span[-1].get_text(strip=True) if comment_span and len(comment_span) > 0 else "No comments found"

    directors = movie_element.find('div', class_='bd').find('p').get_text(strip=True) \
        if movie_element.find('div', class_='bd') and movie_element.find('div', class_='bd').find('p') else "No directors found"

    link_element = movie_element.find('div', class_='pic').find('a') \
        if movie_element.find('div', class_='pic') else None
    link = link_element.get('href') if link_element else "No link found"

    pic_element = movie_element.find('div', class_='pic').find('img') \
        if movie_element.find('div', class_='pic') else None
    pic = pic_element.get('src') if pic_element else "No picture found"

    return title, rating_num, comment_num, directors, link, pic


def process_html_files(directory):
    """
    Processes HTML files in the given directory and extracts movie information.

    Args:
        directory (str): The path to the directory containing HTML files.
    """
    for html_file in os.listdir(directory):
        full_path = os.path.join(directory, html_file)
        if os.path.isfile(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as file_handler:
                    html = file_handler.read()
                    soup = BeautifulSoup(html, 'lxml')
                    movie_list = soup.find('ol', class_='grid_view')
                    if movie_list:
                        for movie in movie_list.find_all('li'):
                            movie_info = extract_movie_info(movie)
                            print(movie_info)
                    else:
                        print(f"No movie list found in {html_file}")
            except PermissionError:
                print(f"Permission denied for {full_path}")
            except Exception as exception:
                print(f"An error occurred while processing {html_file}: {exception}")
        else:
            print(f"Skipping directory: {html_file}")


if __name__ == "__main__":
    process_html_files(DESTINATION_DIRECTORY)