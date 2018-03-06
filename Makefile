imdb.db : subset.py
	sqlite3 imdb_raw_data/imdb.db ".clone imdb.db"
	./subset.py

clean :
	rm imdb.db

rebuild : clean imdb.db
