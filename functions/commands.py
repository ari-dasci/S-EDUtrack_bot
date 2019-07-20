"""Funciones de los comandos establecidos en el bot EDUtrack"""
from telegram  import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang
)
from dictionaries import (
  student_dict_lang as stu_lang
)
from configuration.config_file import client, db
from functions import (
  general_functions as g_fun
)

is_config_files_set = True if (db.students.find_one() and db.activities.find_one()) else False

def start(update, context, pass_chat_data=True):
  """ Inicializa el bot y revisa si se encuentra configurado.

  Se obtienen los datos del estudiante.
  """
  user_first_name = update.message.from_user.first_name
  keyboard = g_lang.language_opt
  reply_markup = IKMarkup(keyboard)
  update.message.reply_text(
      parse_mode = 'HTML',
      text = g_lang.choice_language_text(user_first_name),
      reply_markup = reply_markup)


def press_button(update, context):
  """Recibe la respuesta al presionar un boton del menú."""
  query = update.callback_query
  print("\n\nCHECK QUERY DATA:",query.data)
  selections = (query.data).split('-')
  print("CHECK SELECTIONS", selections)
  choice = selections[-1]
  print("CHECK CHOICE", choice)
  valid_languages = ["ES","EN"]
  if choice in valid_languages:
    user = g_fun.get_user_data(update, choice)
  
  

  if is_config_files_set:
    if g_fun.is_student_registered(update, context, user):      
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
          g_fun.welcome(query, user)    
      else:
        if choice == "suggestion":
          suggestion(query)
        elif choice == "change_language":
          change_language(query)
        elif choice == "actions":
          cmd.actions(update, context)
  else:
    query.edit_message_text(
      parse_mode = "HTML",
      text = g_lang.not_config_files_set_text[user['language']]
    )
   
    
    





if __name__ == '__main__':
    pass