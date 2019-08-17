"""Funciones de los comandos establecidos en el bot EDUtrack"""
import re
import inspect
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)
import configuration.config_file as cfg
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang
)
from configuration.config_file import (
  client, db,
  is_config_files_set)
from functions import (
  general_functions as g_fun,
  teacher_functions as tea_fun
)

def start(update, context, pass_chat_data=True):
  """ Inicializa el bot y revisa si se encuentra configurado.

  Se obtienen los datos del estudiante.
  
  """
  try:
    print("CHECK CMD *** START ***")
    chat_id = update._effective_chat.id
    user = g_fun.get_user_data(update)
    if chat_id  > 0:
      user_first_name = update.message.from_user.first_name
      keyboard = g_lang.language_opt
      reply_markup = IKMarkup(keyboard)
      update.message.reply_text(
          parse_mode = 'HTML',
          text = g_lang.choice_language_text(user_first_name),
          reply_markup = reply_markup)
    else:
      g_fun.msg_wrong_command_group(update, context, user)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def press_button(update, context):
  """Recibe la respuesta al presionar un boton del menú."""
  try:
    print("CHECK CMD *** PRESS BUTTON ***")
    query = update.callback_query
    print("CHECK CMD QUERY DATA:",query.data,"\n")
    selections = (query.data).split('-')
    # print("CHECK SELECTIONS", selections)
    choice = selections[-1]
    # print("CHECK CHOICE", choice)
    valid_languages = ["ES","EN"]
    
    if choice in valid_languages:
      user = g_fun.get_user_data(update, language=choice)
    else:  
      user = g_fun.get_user_data(update)

    if cfg.is_config_files_set:
      if g_fun.is_user_registered(update,context, user):      
        if len(selections) > 1:
          category = selections[0]
          if category == 'stu_menu':
            if selections[1] == "my_grade":
              my_grade(query)
            elif selections[1] == "opn":
              opinion(query, selections)
            elif selections[1]== "eva":
                evaluate(query, selections)
          elif category == "welcome":
            g_fun.welcome(context, query, user)    
        else:
          if choice == "suggestion":
            suggestion(query)
          elif choice == "change_language":
            change_language(query)
          elif choice == "actions":
            cmd.actions(update, context)
    else:
      if user['is_teacher']:
        tea_fun.config_files_set(update, context, user)
      else:
        query.edit_message_text(
          parse_mode = "HTML",
          text = stu_lang.not_config_files_set_text (context, user['language'])
      )
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def check_email(update, context):
  try:
    print("CHECK CMD *** CHECK EMAIL ***")
    chat_id = update._effective_chat.id
    if chat_id > 0:
      if cfg.is_config_files_set:
        user = g_fun.get_user_data(update)
        if len(context.args) ==1:
          email = context.args[0]
          print(email)
          if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
            if db.registered_students.find_one({'_id':user['_id']}):
              g_fun.send_Msg(context, user['_id'], stu_lang.email_is_registered_text(email, user['language']))
              return True
            else:
              if db.students_file.find_one({'_id':email}):
                student = db.students_file.find_one({'_id':email})
                db.registered_students.save({
                  '_id' : user['_id'],
                  'email':email,
                  'name' : student['name'],
                  'telegram_name' : user['telegram_name'],
                  'username' : user['username'],
                  'planet' : user['planet'],
                  'is_teacher' : user['is_teacher'],
                  'language' : user['language']
                })
                g_fun.send_Msg(context, user['_id'])
              else:
                g_fun.send_Msg(context, user['_id'], stu_lang.email_not_found_text(email, user['language']))
          else:
            g_fun.send_Msg(user['_id'], g_lang.email_syntax_error_text(context, user['language'], email))
        elif len(context.args) < 1:
          g_fun.send_Msg(context, user['_id'], stu_lang.check_email_no_args_text[user['language']])
        else:
          g_fun.send_Msg(context, user['_id'], stu_lang.check_email_many_args_text(' '.join(context.args), user['language']))
      else:
        g_fun.send_Msg(context, chat_id, stu_lang.not_config_files_set_text (context, user['language']))
    else:
      g_fun.send_Msg(context, chat_id, g_lang.wrong_command_group[user['language']])
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def change_language(update, context):
  try:
    chat_id = update._effective_chat.id
    user = g_fun.get_user_data(update)
    if chat_id > 0:
      if db.telegram_users.find_one({'_id':user['_id']}):
        user = db.telegram_users.find_one({'_id':user['_id']})
        current_lang = user['language']
        new_lang = "EN" if current_lang == "ES" else "ES"
        db.telegram_users.update_one({'_id':user['_id']},
          {'$set':{
            'language':new_lang}})
        g_fun.send_Msg(context, chat_id, g_lang.cmd_change_language_text[user['language']])
    else:
      g_fun.send_Msg(context, chat_id, g_lang.wrong_command_group[user['language']])
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")




if __name__ == '__main__':
    pass