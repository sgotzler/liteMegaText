# liteMegaText

Repo for creating SQLite Megatext dB Clones

This requires sqlite3, python3 and the original IMDB database downloaded on 9/17.

Everything else is self-contained.

Steps:

1. Update line of Makefile to point to location of imdb.db (note: I'm working off of an 1/18 iteration of the db but this should work with the original 09/17 IMDB database)

2. From command line run `make imdb.db` to build initial db and ` make rebuild` for fresh wipe of db.

Misc notes:

- linktbl.csv contains all deduped ids and uids, linktbls.csv only contains matches.
- enc.csv contains working version of Vincent Terrace's encyclopedia.
