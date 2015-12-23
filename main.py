import time
import requests
import mysql.connector


class Parser:
    def __init__(self):
        self.base_url = 'http://api.themoviedb.org/3/discover/movie?api_key=YOUR_THEMOVIEDB_KEY' \
                        '&language=ru&include_adult=true&page='
        self.total_pages = self.get_total_pages()
        self.results = []

    def get_total_pages(self):
        return requests.get(self.base_url).json()['total_pages']

    def get_all_results(self, first_page=None, stop_page=None):
        conn = mysql.connector.connect(host='localhost', database='films', user='root', password='')
        cursor = conn.cursor()
        if not stop_page:
            stop_page = self.total_pages
        for page in range(int(first_page), int(stop_page) + 1):
            percent =  (page / stop_page) * 100
            print('Now %s from %s' % (page, self.total_pages))
            print('%s percent completed' % (str(percent)))
            temp = requests.get('%s%s' % (self.base_url, page)).json()['results']
            time.sleep(0.3)
            for film in temp:
                query = "SELECT * FROM `films` WHERE `id`='%s'" % film['id']
                cursor.execute(query)
                cursor.fetchall()

                if cursor.rowcount == 0:
                    cursor.execute(
                        "INSERT INTO `films` (`id`, `original_title`, `title`, `overview`, `video`, `backdrop_path`, "
                        "`poster_path`, `release_date`, `original_language`, `adult`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (film['id'], film['original_title'], film['title'], film['overview'], film['video'],
                         film['backdrop_path'], film['poster_path'], film['release_date'],
                         film['original_language'], film['adult']))
                    print(film['original_title'])
        return 0


if __name__ == "__main__":

    p = Parser()
    num = p.get_total_pages()
    p.get_all_results(1, num)

