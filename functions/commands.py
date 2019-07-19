def start(update, context, pass_chat_data=True):
  """ Inicializa el bot y saluda."""
  user_first_name = update.message.from_user.first_name
  print(user_first_name)
  chat_id = update.message.chat_id
  context.bot.send_message(
    chat_id = chat_id,
    text = f"Hola {user_first_name}. Soy tu asistente EDUtrack."
  )
  


if __name__ == '__main__':
    pass