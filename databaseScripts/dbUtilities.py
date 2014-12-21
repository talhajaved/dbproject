import psycopg2 as pg
import config

def deleteDB():
  conn = pg.connect(database=config.db['default-db'], user=config.db['user'], password=config.db['password'],\
    host =config.db['host'])
  conn.set_isolation_level(0);
  cur = conn.cursor()
  cur.execute("DROP DATABASE IF EXISTS "+config.db['db']+";")
  conn.commit()
  conn.set_isolation_level(1);
  cur.close()
  conn.close()

def createDB():
  conn = pg.connect(database=config.db['default-db'], user=config.db['user'],\
    password=config.db['password'], host =config.db['host'])
  conn.set_isolation_level(0);
  cur = conn.cursor()
  cur.execute("CREATE DATABASE "+config.db['db']+";")
  conn.set_isolation_level(1);
  cur.close()
  conn.close()
