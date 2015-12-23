# themoviedb_get_all_movies
Get all movies from themoviedb.org

for correct working you nedd to push your themoviedb.org key into 
```
  self.base_url = 'http://api.themoviedb.org/3/discover/movie?api_key=YOUR_THEMOVIEDB_KEY' \
  '&language=ru&include_adult=true&page='
```
and set up mysql connection
```
conn = mysql.connector.connect(host='localhost', database='films', user='root', password='') 
```
