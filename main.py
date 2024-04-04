import logging
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

BOT_TOKEN = '6610676706:AAEKHc-7_1cn21Fns8FM0Gildh6n3Jx8q30'

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "Вы можете пропустить вопрос, послав команду /skip.\n"
        "В каком городе вы живёте?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


async def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    await update.message.reply_text(
        f"Какая погода в городе {locality}?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


async def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    logger.info(weather)
    await update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def skip_city(update, context):
    await update.message.reply_text(
        f"Какая погода у вас в городе?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points = [CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states = {
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response), CommandHandler('skip', skip_city)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        fallbacks = [CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
