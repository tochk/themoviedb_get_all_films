from classes.Parser import Parser
import mysql.connector

if __name__ == "__main__":
    api_key = '' #themoviedb api key
    mysql_host = 'localhost'
    mysql_db = 'movies'
    mysql_login = 'root'
    mysql_password = ''
    mysql_port = '3306'
    language = 'ru'
    debug_level = 0

    conn = mysql.connector.connect(host=mysql_host, database=mysql_db, user=mysql_login, password=mysql_password,
                                   port=mysql_port)
    cursor = conn.cursor()
    parser = Parser(api_key, language, debug_level)
    stop_movie_page = parser.get_total_movies_pages()
    parser.get_all_genres(cursor)
    parser.get_movies(None, None, cursor)
    parser.get_series(None, None, cursor)



