from telegram.ext import MessageHandler, CommandHandler, filters
from telegram import BotCommand
from config.telegram_bot import application
from handlers.message_handlers import chatgpt_reply
from handlers.command_handlers import *

# Регистрация обработчика текстовых сообщений
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply)
application.add_handler(message_handler)

# Регистрация обработчика команд
start_command_handler = CommandHandler("start", start_reply)
application.add_handler(start_command_handler)

motivate_command_handler = CommandHandler("motivate", motivate_reply)
application.add_handler(motivate_command_handler)

sdvg_command_handler = CommandHandler("sdvg", sdvg_reply)
application.add_handler(sdvg_command_handler)

get_docs_command_handler = CommandHandler("get_docs", get_docs_reply)
application.add_handler(get_docs_command_handler)

help_command_handler = CommandHandler("help", help_reply)
application.add_handler(help_command_handler)

meme_command_handler = CommandHandler("meme", meme_reply)
application.add_handler(meme_command_handler)

# Запуск бота
application.run_polling()