import contextlib
import inspect
import os
import pandas as pd
import sqlite3
import sys
import config.config_file as cfg
from functions import general_functions as g_fun

db_path = f"./DB/{cfg.subject_data['_id']}.db"


def connection(open_connection="False"):
  conn = sqlite3.connect(db_path)
  print("Conexión exitosa")
  return conn if open_connection else conn.close()


def execute_statement(sql_query, fetch=False, df=False):
  try:
    # auto - closes
    with contextlib.closing(sqlite3.connect(db_path)) as conn:
      with conn:  # auto - commits
        with contextlib.closing(conn.cursor()) as cursor:  # auto - closes
          ######### COMPROBACION CURSOR
          if fetch:
            cursor.execute(sql_query)
            print(
              "PRUEBA CURSOR: ",
              cursor.fetchone() if fetch == "fetchone" else cursor.fetchall(),
            )
          ###############################
          cursor.execute(sql_query)
          if fetch:
            return cursor.fetchone() if fetch == "fetchone" else cursor.fetchall()
          elif df:
            return pd.read_sql_query(sql_query, con=conn)
          return True
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def create_db():
  try:
    for table in cfg.tables:
      sql = f"""CREATE TABLE if not exists {table['name']} ({table['fields']})"""
      execute_statement(sql)
      print(f"Se ha agregado la tabla {table['name']} a la base de datos")

    # sql = f"""INSERT INTO telegram_users VALUES (
    sql = f"""INSERT OR IGNORE INTO telegram_users VALUES (
      {int(cfg.teacher_data['_id'])},
      '{cfg.teacher_data['telegram_name']}',
      '{cfg.teacher_data['username']}',
      {int(cfg.teacher_data['is_teacher'])},
      '{cfg.teacher_data['language']}')"""
    execute_statement(sql)

    # sql = f"""INSERT INTO teachers VALUES(
    sql = f"""INSERT OR IGNORE INTO teachers VALUES(
      {int(cfg.teacher_data['_id'])},
      '{cfg.teacher_data['telegram_name']}',
      '{cfg.teacher_data['username']}',
      '{cfg.teacher_data['email']}'
      )"""
    execute_statement(sql)
    print(f"Se agrego correctamente al docente {cfg.teacher_data['telegram_name']}.")

    sql = "SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='teachers_temp'"
    if execute_statement(sql, "fetchone")[0]:
      sql = f"SELECT COUNT(*) FROM teachers_temp"
      if execute_statement(sql, "fetchone")[0]:
        cfg.standby_teachers = True

    # TRIGGER to update username in telegram_users
    sql = f"""CREATE TRIGGER IF NOT EXISTS telegram_username
              AFTER UPDATE ON telegram_users
              WHEN t.username <> r.username
              BEGIN
                INSERT INTO registered_students (t_username, r_username, tipo_operacion, fecha_cambio)
              VALUES
                (t.username, r.username, 'UPDATE',DATETIME('NOW'));
              """

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def get_columns_names(table_name):
  try:
    sql = f"PRAGMA table_info({table_name});"
    column_names = [x[1] for x in execute_statement(sql, fetch="fetchall")]
    print(column_names)
    return column_names
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)

def save_config_file_DB(df, table_name, action="replace"):
  try:
    conn = connection(True)
    df.to_sql(table_name, con=conn, index=False, if_exists=action)
    conn.close()
    return True
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False

# REVISAR SI SIRVE
""" def is_user_registered(user):
  try:
    sql = f"SELECT count(*) FROM registered_students WHERE _id={user._id}"
    return True if execute_statement(sql, "fetchone") else False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path) """
