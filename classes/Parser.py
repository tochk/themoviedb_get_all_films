import time

import requests


class Parser:
    def __init__(self, api_key, language, debug_level):
        self.base_movies_url = (
            'http://api.themoviedb.org/3/discover/movie?api_key=%s&language=%s&page=' % (api_key, language))
        self.base_series_url = (
            'http://api.themoviedb.org/3/discover/tv?api_key=%s&language=%s&page=' % (api_key, language))
        self.base_movies_genres_url = (
            'http://api.themoviedb.org/3/genre/movie/list?api_key=%s&language=%s' % (api_key, language))
        self.base_series_genres_url = (
            'http://api.themoviedb.org/3/genre/tv/list?api_key=%s&language=%s' % (api_key, language))

        self.total_movies_pages = self.get_total_movies_pages()
        self.total_series_pages = self.get_total_series_pages()
        self.debug_level = debug_level

    def get_total_movies_pages(self):
        return requests.get(self.base_movies_url).json()['total_pages']

    def get_total_series_pages(self):
        return requests.get(self.base_series_url).json()['total_pages']

    def get_all_genres(self, cursor):
        inserted = 0
        updated = 0
        for genre_list in (self.base_movies_genres_url, self.base_series_genres_url):
            genres = requests.get(genre_list).json()['genres']
            for genre in genres:
                cursor.execute("SELECT `name` FROM `genres` WHERE `id`=%s" % (genre['id']))
                cursor.fetchall()
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO `genres` (`id`, `name`) VALUES (%s, %s)", (genre['id'], genre['name']))
                    if self.debug_level >= 1:
                        print("Inserted genre %s" % (genre['name']))
                    inserted += 1
                else:
                    cursor.execute("UPDATE `genres` SET `name` = %s WHERE `id` = %s", (genre['name'], genre['id']))
                    if self.debug_level >= 2:
                        print("Updated genre %s" % (genre['name']))
                    updated += 1
            time.sleep(0.3)
        print("Inserted %d genres \nUpdated %d genres" % (inserted, updated))

    def get_movies(self, first_page=None, stop_page=None, cursor=None):
        inserted = 0
        updated = 0
        if not first_page:
            first_page = 1
        if not stop_page:
            stop_page = self.total_movies_pages
        if not cursor:
            print("Mysql error")
            return
        for page in range(int(first_page), int(stop_page) + 1):
            percent = round((page / stop_page) * 100, 3)
            try:
                print('%s percent completed (%s from %s)' % (str(percent), page, stop_page))
                results = requests.get('%s%s' % (self.base_movies_url, page)).json()['results']
                time.sleep(0.3)
                for movie in results:
                    cursor.execute("SELECT `title` FROM `movies` WHERE `id`='%s'" % movie['id'])
                    cursor.fetchall()
                    if cursor.rowcount == 0:
                        cursor.execute(
                            "INSERT INTO `movies` (`id`, `original_title`, `title`, `overview`, "
                            "`poster_path`, `release_date`, `original_language`, `popularity`,"
                            "`vote_count`, `vote_average`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (movie['id'], movie['original_title'], movie['title'], movie['overview'],
                             movie['poster_path'], movie['release_date'], movie['original_language'],
                             movie['popularity'], movie['vote_count'], movie['vote_average']))
                        for genre in movie['genre_ids']:
                            try:
                                cursor.execute(
                                    "INSERT INTO `genre_movies_merge` (`id`, `genreid`) VALUES (%s, %s)",
                                    (movie['id'], genre)
                                )
                            except:
                                print("Already in DB")
                        inserted += 1
                        try:
                            if self.debug_level >= 1:
                                print("INSERTED: %s" % (movie['title']))
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
                    else:
                        cursor.execute(
                            "UPDATE `movies` SET `title` = %s, `original_title` = %s,  `overview` = %s, "
                            "`poster_path` = %s, `release_date` = %s, `original_language` = %s, `popularity` = %s, "
                            "`vote_count` = %s, `vote_average` = %s WHERE `movies`.`id` = %s",
                            (movie['title'], movie['original_title'], movie['overview'], movie['poster_path'],
                             movie['release_date'],
                             movie['original_language'], movie['popularity'], movie['vote_count'],
                             movie['vote_average'], movie['id']))
                        for genre in movie['genre_ids']:
                            try:
                                cursor.execute(
                                    "INSERT INTO `genre_movies_merge` (`id`, `genreid`) VALUES (%s, %s)",
                                    (movie['id'], genre)
                                )
                            except:
                                print("Already in DB")
                        updated += 1
                        try:
                            if self.debug_level >= 2:
                                print("UPDATED: %s" % (movie['title']))
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
            except KeyError:
                print('KeyError')
        print("Inserted %d movies \nUpdated %d movies" % (inserted, updated))
        return 0

    def get_series(self, first_page=None, stop_page=None, cursor=None):
        inserted = 0
        updated = 0
        if not first_page:
            first_page = 1
        if not stop_page:
            stop_page = self.total_series_pages
        if not cursor:
            print("Mysql error")
            return
        for page in range(int(first_page), int(stop_page) + 1):
            percent = round((page / stop_page) * 100, 3)
            try:
                print('%s percent completed (%s from %s)' % (str(percent), page, stop_page))
                results = requests.get('%s%s' % (self.base_series_url, page)).json()['results']
                time.sleep(0.3)
                for tv in results:
                    cursor.execute("SELECT `title` FROM `series` WHERE `id`='%s'", tv['id'])
                    cursor.fetchall()
                    if cursor.rowcount == 0:
                        cursor.execute(
                            "INSERT INTO `series` (`id`, `original_title`, `title`, `overview`, `first_air_date`,"
                            "`poster_path`, `original_language`,  `popularity`, `vote_count`, `vote_average`)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (tv['id'], tv['original_name'], tv['name'], tv['overview'], tv['first_air_date'],
                             tv['poster_path'], tv['original_language'],  tv['popularity'], tv['vote_count'],
                             tv['vote_average']))
                        for genre in tv['genre_ids']:
                            cursor.execute(
                                "INSERT INTO `genre_series_merge` (`id`, `genreid`) VALUES (%s, %s)",
                                (tv['id'], genre)
                            )
                        inserted += 1
                        try:
                            if self.debug_level >= 1:
                                    print("INSERTED: %s" % (tv['name']))
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
                    else:
                        cursor.execute(
                            "UPDATE `series` SET `original_title` = %s, `title` = %s, `overview` = %s, "
                            "`first_air_date` = %s, `poster_path` = %s, `original_language` = %s, `popularity` = %s, "
                            "`vote_count` = %s, `vote_average` = %s WHERE `movies`.`id` = %s",
                            (tv['original_name'], tv['name'], tv['overview'], tv['first_air_date'],
                             tv['poster_path'], tv['original_language'],  tv['popularity'], tv['vote_count'],
                             tv['vote_average'], tv['id']))
                        for genre in tv['genre_ids']:
                            try:
                                cursor.execute(
                                    "INSERT INTO `genre_series_merge` (`id`, `genreid`) VALUES (%s, %s)",
                                    (tv['id'], genre)
                                )
                            except:
                                if self.debug_level >= 2:
                                    print("Already in DB")
                        updated += 1
                        try:
                            if self.debug_level >= 2:
                                print("UPDATED: %s" % (tv['title']))
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
            except KeyError:
                print('KeyError')
        print("Inserted %d series \nUpdated %d series" % (inserted, updated))
        return 0
