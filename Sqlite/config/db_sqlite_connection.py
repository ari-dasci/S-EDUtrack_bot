import contextlib
import inspect
import os
import sqlite3
import sys

import pandas as pd

import config.config_file as cfg
from functions import general_functions as g_fun

db_path = f"./DB/{cfg.subject_data['_id']}.db"


def connection(open_connection="False"):
  conn = sqlite3.connect(db_path)
  print("Conexión exitosa")
  return conn if open_connection else conn.close()


def execute_sql(
  sql_query, fetch=False, df=False, as_dict=False, as_list=False, test=False
):  ### BORRAR TEST
  try:
    # auto - closes
    with contextlib.closing(sqlite3.connect(db_path)) as conn:
      with conn:  # auto - commits
        if as_dict:
          conn.row_factory = sqlite3.Row
        if as_list:
          conn.row_factory = lambda cursor, row: row[0]
        with contextlib.closing(conn.cursor()) as cursor:  # auto - closes
          ######### COMPROBACION CURSOR
          if test:
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
    g_fun.print_except(error_path, sql_query)
    raise


def create_db():
  try:
    # CREATE TABLES
    for table in cfg.tables:
      sql = f"""CREATE TABLE if not exists {table} ({cfg.tables[table]})"""
      execute_sql(sql)
      print(f"Se ha agregado la tabla {table} a la base de datos")

    # SET SUBJECT DATA
    sql = f"""INSERT INTO subject_data VALUES {tuple(cfg.subject_data.values())}"""

    execute_sql(sql)

    # sql = f"""INSERT INTO teachers VALUES(
    sql = f"""INSERT OR IGNORE INTO teachers VALUES(
      "{cfg.teacher_data['email']}",
      "{cfg.teacher_data['telegram_name']}",
      "{cfg.teacher_data['username']}",
      "{int(cfg.teacher_data['telegram_id'])}"
      )"""
    execute_sql(sql)
    print(f"Se agrego correctamente al docente {cfg.teacher_data['telegram_name']}.")

    sql = f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='teachers_temp'"
    if execute_sql(sql, "fetchone")[0]:
      sql = f"SELECT COUNT(*) FROM teachers_temp"
      if execute_sql(sql, "fetchone")[0]:
        cfg.standby_teachers = True

    for trigger in cfg.triggers:
      sql = trigger
      execute_sql(sql)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def get_columns_names(table_name):
  try:
    sql = f"PRAGMA table_info({table_name});"
    column_names = [x[1] for x in execute_sql(sql, fetch="fetchall")]
    return column_names
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def save_file_in_DB(df, table_name, index=False, action="replace"):
  try:
    conn = connection(True)
    df.to_sql(table_name, con=conn, index=index, if_exists=action)
    conn.close()
    return True
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def save_elements_in_DB(df_to_save, table_name):
  try:
    conn = connection(True)

    df_backup = table_DB_to_df(table_name)
    df_to_save.to_sql("delete", con=conn, index=False, if_exists="replace")
    sql = f"DELETE FROM {table_name}"
    execute_sql(sql)
    sql = f"INSERT INTO {table_name} SELECT * FROM 'delete'"
    execute_sql(sql)
    sql = f"DROP TABLE IF EXISTS 'delete'"
    execute_sql(sql)
    return True
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    save_elements_in_DB(df_backup, table_name)
    raise


def table_DB_to_df(table_name, columns="*", sql=False, index=False):
  try:
    if not sql:
      sql = f"SELECT {columns} FROM {table_name}"
    df = execute_sql(sql, df=True)
    if index:
      if isinstance(index, str):
        df.set_index(index, inplace=True)
      else:
        ID = df.columns[0]
        df.set_index(ID, inplace=True)
    return df
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def change_primary_key(table_name, old_value, new_value):
  try:
    df_table = table_DB_to_df(table_name)
    primary_key = df_table.columns[0]
    row_index = df_table[df_table[primary_key] == old_value].index[0]
    df_table.loc[row_index, (primary_key)] = new_value
    save_elements_in_DB(df_table, table_name)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False
