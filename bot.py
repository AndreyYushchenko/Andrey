import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Установите ваш токен от BotFather
TELEGRAM_TOKEN = '8133198843:AAE_DLqJpK3k_O0MuyLSs_90lhWQG8x8H_k'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для подтверждения оплаты. Пожалуйста, отправьте подтверждение оплаты.')

def handle_message(update: Update, context: CallbackContext) -> None:
    # Это место, где можно обработать подтверждения платежа
    user_message = update.message.text
    if 'платеж' in user_message.lower():  # Пример условия для подтверждения
        update.message.reply_text('Ваш платеж подтвержден!')
        # Можно добавить логику для уведомления администратора (например, отправка вам сообщения)
    else:
        update.message.reply_text('Пожалуйста, отправьте сообщение с подтверждением платежа.')

def main() -> None:
    # Запуск бота
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
