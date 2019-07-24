from configuration.config_file import (
  db, client)
from functions import (
  general_functions as g_fun
)
from dictionaries import (
  teacher_dict_lang as tea_lang
)


def config_files_set(update, context, user):
  print("CHECK   ENTRO EN CONFIG FILES SET")
    #print("CONTROL SI ES DOCENTE")
  if not db.students.find_one() and not db.activities.find_one():
    #print("   CONTROL NO HAY NINGUN ARCHIVO CONFIGURADO")
    download_config_files(update, context, user)
  else:
    if not db.students.find_one():
      context.send_message(
        chat_id = user['_id'],
        parse_mode = 'HTML',
        text = tea_lang.config_file_set_text ('students', user)) 
      students_format(update, context)
    elif not db.activities.find_one():
      bot.sendMessage(
        chat_id = user['_id'],
        parse_mode = 'HTML',
        text = tea_lang.config_file_set_text ('activities', user))
      activities_format(update, context)
  
def download_config_files(update, context, user):
  context.bot.send_message(
    chat_id = user['_id'],
    parse_mode = "HTML",
    text = tea_lang.download_config_files_text[user['language']])
  students_format(update, context, user)
  activities_format(update, context, user)

def students_format(update, context, user, query=""):
  chat_id = update._effective_chat.id
  context.bot.send_document(chat_id=user['_id'], document=open(
    "files/guides/students_format.csv", 'rb'))
  if chat_id < 0:
    context.bot.send_message(
      chat_id=chat_id,
      text="Se envio el archivo al chat privado")
  print("Se preparo el archivo students_format para ser descargado")

def activities_format(update, context, user, query=""):
  chat_id = update._effective_chat.id
  context.bot.send_document(chat_id=user['_id'], document=open(
    "files/guides/activities_format.csv", 'rb'))

  if chat_id < 0:
    context.bot.send_message(
      chat_id=user['_id'],
      text="Se envio el archivo al chat privado")
  print("Se preparo el archivo activities_format para ser descargado")

