import contextlib
import os
import sqlite3
import sys
import config.config_file as cfg

db_path = f"./DB/{cfg.subject_data['id']}.db"


def connection():
  connection = sqlite3.connect(db_path)
  print("Conexión establecida exitosamente.")
  connection.close()


def execute_statement(sql_query, fetch=False):
  try:
    # auto - closes
    with contextlib.closing(sqlite3.connect(db_path)) as conn:
      with conn:  # auto - commits
        with contextlib.closing(conn.cursor()) as cursor:  # auto - closes
          cursor.execute(sql_query)
          if fetch:
            return cursor.fetchone() if fetch == "fetchone" else cursor.fetchall()
          return True
  except Exception as e:
    print(f"The error '{e}' occurred")


def create_db():
  try:
    for table in cfg.tables:
      sql = f"""CREATE TABLE if not exists {table['name']} ({table['fields']})"""
      execute_statement(sql)
      print(f"Se ha agregado la tabla {table['name']} a la base de datos")

    sql = f"""INSERT INTO telegram_users VALUES (
      {int(cfg.teacher_data['id_telegram'])},
      '{cfg.teacher_data['telegram_name']}',
      '{cfg.teacher_data['username']}',
      {int(cfg.teacher_data['is_teacher'])},
      '{cfg.teacher_data['language']}')"""
    execute_statement(sql)

    sql = f"""INSERT INTO teachers VALUES(
      {int(cfg.teacher_data['id_telegram'])},
      '{cfg.teacher_data['telegram_name']}',
      '{cfg.teacher_data['username']}',
      '{cfg.teacher_data['email']}'
      )"""

    execute_statement(sql)
    print(f"Se agrego correctamente al docente {cfg.teacher_data['telegram_name']}.")
  except Exception as e:
    print(e)


def get_colums_names(table_name):
  sql = f"PRAGMA table_info({table_name});"
  column_names = [x[1] for x in execute_statement(sql, fetch="fetchall")]
  print(column_names)
  return column_names
