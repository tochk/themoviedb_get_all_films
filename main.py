from classes.ParserMovies import ParserMovies
from classes.ParserTv import ParserTv


if __name__ == "__main__":

    api_key = '' #themoviedb api key
    mysql_host = 'localhost'
    mysql_db = 'movies'
    mysql_login = 'root'
    mysql_password = ''

    movies = ParserMovies(api_key)
    num = movies.get_total_pages()
    movies.get_all_results(1, num, mysql_host, mysql_db, mysql_login, mysql_password)

    tv = ParserTv(api_key)
    num = tv.get_total_pages()
    tv.get_all_results(1, num, mysql_host, mysql_db, mysql_login, mysql_password)