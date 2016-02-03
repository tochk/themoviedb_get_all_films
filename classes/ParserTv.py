import time
import requests
import mysql.connector


class ParserTv:
    def __init__(self, api_key):
        self.base_url = ('http://api.themoviedb.org/3/discover/tv?api_key=%s&language=ru&include_adult=true&page=' % api_key)
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
            except KeyError:
                print('KeyError')
            temp = requests.get('%s%s' % (self.base_url, page)).json()['results']
            time.sleep(0.3)
            for tv in temp:
                query = "SELECT * FROM `tv` WHERE `id`='%s'" % tv['id']
                cursor.execute(query)
                cursor.fetchall()

                if cursor.rowcount == 0:
                    cursor.execute(
                        "INSERT INTO `tv` (`id`, `original_name`, `name`, `overview`, `first_air_date`, `backdrop_path`, "
                        "`poster_path`, `original_language`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (tv['id'], tv['original_name'], tv['name'], tv['overview'], tv['first_air_date'],
                         tv['backdrop_path'], tv['poster_path'], tv['original_language']))
                    try:
                        print(tv['name'])
                    except UnicodeEncodeError:
                        print('UnicodeEncodeError')
                    conn.commit()
        return 0

