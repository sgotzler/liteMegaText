#! /usr/bin/env python3


# This is the original build code.  Adopted from http://eeyore.ucdavis.edu/stat141/Hws/imdb.html

import sqlite3, csv

# Connect to db

c = sqlite3.connect('imdb.db')
conn = c.cursor()

# build tables, set year range and kind_id

def update_tables():
    conn.execute('''
    CREATE TABLE IF NOT EXISTS  title2 AS
    SELECT * FROM title
     WHERE production_year >= 1940 AND production_year < 1960
       AND  (kind_id IN (2, 3, 5, 7));''')


    conn.execute('''
    CREATE TABLE IF NOT EXISTS  movie_keyword2 AS
      SELECT * FROM movie_keyword
       WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  keyword2 AS
      SELECT * FROM keyword
       WHERE id IN (SELECT keyword_id FROM movie_keyword2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  aka_title2 AS
      SELECT * FROM aka_title
       WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  cast_info2 AS
      SELECT * FROM cast_info
       WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  movie_info2 AS
      SELECT * FROM movie_info
       WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  movie_info_idx2 AS
      SELECT * FROM movie_info_idx
       WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  name2 AS
      SELECT * FROM name
       WHERE id IN (SELECT person_id FROM cast_info2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  aka_name2 AS
      SELECT * FROM aka_name
       WHERE person_id IN (SELECT id FROM name2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS  person_info2 AS
      SELECT * FROM person_info
       WHERE person_id IN (SELECT id FROM name2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS movie_companies2 AS
      SELECT * FROM movie_companies
      WHERE movie_id IN (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS company_name2 AS
      SELECT * FROM company_name
      WHERE id IN (SELECT company_id FROM movie_companies2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS company_type2 AS
      SELECT * FROM company_type
      WHERE id IN (SELECT company_type_id FROM movie_companies2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS role_type2 AS
        SELECT * FROM role_type
        WHERE id IN (SELECT role_id FROM cast_info2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS char_name2 AS
        SELECT * FROM char_name
        WHERE id IN (SELECT person_role_id FROM cast_info2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS complete_cast2 AS
      SELECT * FROM complete_cast
      WHERE movie_id IN  (SELECT id FROM title2);''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS comp_cast_type2 AS
        SELECT * FROM comp_cast_type
        WHERE id IN  (SELECT status_id FROM complete_cast2);''')

    c.commit()


# create enc and linktbl

def update_enc():
    f=open('enc.csv','r', encoding = 'ISO-8859-1') # open the csv data file
    next(f, None) # skip the header row
    reader = csv.reader(f)

    conn.execute('''
    CREATE TABLE IF NOT EXISTS encyclopedia (
      uid INTEGER,
      program_title INTEGER,
      program_type INTEGER,
      program_genre TEXT,
      network INTEGER,
      first_air_month INTEGER,
      first_air_day TEXT,
      first_air_year INTEGER,
      last_air_month INTEGER,
      last_air_day TEXT,
      last_air_year INTEGER,
      program_description INTEGER
    );''')


    for row in reader:
    	conn.execute('''INSERT OR IGNORE INTO encyclopedia(uid, program_title, program_type, program_genre, network, first_air_month, first_air_day, first_air_year, last_air_month, last_air_day, last_air_year, program_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
    c.commit()

def update_linktbl():
    b=open('linktbls.csv','r', encoding = 'latin1') # open the csv data file
    next(b, None) # skip the header row
    reader = csv.reader(b)

    conn.execute('''
      CREATE TABLE IF NOT EXISTS linktbl (
        uid INTEGER,
        id INTEGER);''')



    for row in reader:
      	conn.execute('''INSERT INTO linktbl(uid,id) VALUES (?, ?)''', row)
    c.commit()



#create indices

def update_indices():
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_name ON name2 (name);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_imdb_id ON name2 (imdb_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_pcodecf ON name2 (name_pcode_cf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_pcodenf ON name2 (name_pcode_nf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_pcode ON name2 (surname_pcode);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS name_idx_md5 ON name2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS char_name_idx_name ON char_name2 (name);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS char_name_idx_pcodenf ON char_name2 (name_pcode_nf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS char_name_idx_pcode ON char_name2 (surname_pcode);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS char_name_idx_md5 ON char_name2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS company_name_idx_name ON company_name2 (name);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS company_name_idx_pcodenf ON company_name2 (name_pcode_nf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS company_name_idx_pcodesf ON company_name2 (name_pcode_sf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS company_name_idx_md5 ON company_name2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_title ON title2 (title);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_imdb_id ON title2 (imdb_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_pcode ON title2 (phonetic_code);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_epof ON title2 (episode_of_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_season_nr ON title2 (season_nr);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_episode_nr ON title2 (episode_nr);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS title_idx_md5 ON title2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_name_idx_person ON aka_name2 (person_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_name_idx_pcodecf ON aka_name2 (name_pcode_cf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_name_idx_pcodenf ON aka_name2 (name_pcode_nf);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_name_idx_pcode ON aka_name2 (surname_pcode);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_name_idx_md5 ON aka_name2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_title_idx_movieid ON aka_title2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_title_idx_pcode ON aka_title2 (phonetic_code);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_title_idx_epof ON aka_title2 (episode_of_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS aka_title_idx_md5 ON aka_title2 (md5sum);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS cast_info_idx_pid ON cast_info2 (person_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS cast_info_idx_mid ON cast_info2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS cast_info_idx_cid ON cast_info2 (person_role_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS complete_cast_idx_mid ON complete_cast2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS keyword_idx_keyword ON keyword2 (keyword);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS keyword_idx_pcode ON keyword2 (phonetic_code);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_keyword_idx_mid ON movie_keyword2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_keyword_idx_keywordid ON movie_keyword2 (keyword_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_info_idx_mid ON movie_info2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_info_idx_idx_mid ON movie_info_idx2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_info_idx_idx_infotypeid ON movie_info_idx2 (info_type_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_info_idx_idx_info ON movie_info_idx2 (info);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_companies_idx_mid ON movie_companies2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS movie_companies_idx_cid ON movie_companies2 (company_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS person_info_idx_pid ON person_info2 (person_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS  uid ON encyclopedia (uid);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS  id ON aka_title2 (movie_id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS  id ON title2 (id);''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS uid on linktbl (uid)''')

    c.commit()

# drop original tables

def drop_tables():
    conn.execute('''
    DROP TABLE IF EXISTS title;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS person_info;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS aka_name;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS aka_title;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS movie_keyword;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS movie_info;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS movie_info_idx;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS keyword;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS cast_info;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS name;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS movie_companies;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS company_name;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS company_type;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS role_type;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS char_name;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS complete_cast;
    ''')
    conn.execute('''
    DROP TABLE IF EXISTS comp_cast_type;
    ''')
    c.commit()

#execute all scripts


def update_all():
    update_tables()
    update_linktbl()
    update_enc()
    update_indices()
    drop_tables()

if __name__ == "__main__":
    update_all()
    print("database build complete!")

conn.close()
