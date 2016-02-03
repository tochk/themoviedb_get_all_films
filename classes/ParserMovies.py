import time
import requests
import mysql.connector


class ParserMovies:
    def __init__(self, api_key):
        self.base_url = ('http://api.themoviedb.org/3/discover/movie?api_key=%s&language=ru&include_adult=true&page=' % api_key)
        self.total_pages = self.get_total_pages()

    def get_total_pages(self):
        return requests.get(self.base_url).json()['total_pages']

    def get_all_results(self, first_page=None, stop_page=None, mysql_host=None, mysql_db=None, mysql_login=None, mysql_password=None):
        conn = mysql.connector.connect(host=mysql_host, database=mysql_db, user=mysql_login, password=mysql_password)
        cursor = conn.cursor()
        if not stop_page:
            stop_page = self.total_pages
        for page in range(int(first_page), int(stop_page) + 1):
            percent = (page / stop_page) * 100
            try:
                print('%s percent completed (%s from %s)' % (str(percent), page, self.total_pages))
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
                        try:
                            print(film['title'])
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
                        conn.commit()
            except KeyError:
                print('KeyError')

        return 0