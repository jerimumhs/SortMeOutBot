from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

from csv_module import save_info

logger = logging.getLogger(__name__)

FULLNAME, EMAIL = range(2)
SEND_ID = 00000000 
dict_user = {}

def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(
        f'Ola {user.full_name}. Seja bem vind@ ao bot de sorteio do Jerimum Hackerspace.'
        'Envie /cancel para encerrar nossa conversa.\n\n'
        'Por favor, digite seu nome completo.')
    dict_user[user.id] = {}
    return FULLNAME


def full_name(bot, update):
    user = update.message.from_user
    logger.info(f'NAME: {user.id} - {user.full_name}: {update.message.text}')
    dict_user[user.id]['user'] = user.full_name
    dict_user[user.id]['fullname'] = update.message.text
    update.message.reply_text('Okay! Agora que temos seu nome, vamos precisar do seu email!')

    return EMAIL


def email(bot, update):
    user = update.message.from_user
    logger.info(f'EMAIL: {user.id} - {user.full_name}: {update.message.text}')
    dict_user[user.id]['email'] = update.message.text
    update.message.reply_text('Show! Agora você está participando do sorteio!')

    bot.send_message(chat_id=user.id,
                     text="Entre no grupo e aguarde os proximos passos. " 
                     "[Clique aqui para entrar!](https://link.do.grupo).",
                     parse_mode=ParseMode.MARKDOWN)
    save = dict_user[user.id]
    save_info([user.id, save['user'], save['fullname'], save['email']])
    bot.send_message(chat_id=SEND_ID,
                     text="Arquivo atualizado!")
    bot.send_document(chat_id=SEND_ID, document=open('inscricoes.csv', 'rb'))
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info(f'CANCEL: {user.id} - {user.full_name}')
    update.message.reply_text('Não tem problema! Quando estiver pronto, basta enviar /start para começar novamente.')
    
    del dict_user[user.id]

    return ConversationHandler.END


def error(bot, update, error):
    logger.warning(f'Update {update} caused error {error}')


def main():
    updater = Updater("<TOKEN>")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            FULLNAME: [MessageHandler(Filters.text, full_name)],

            EMAIL: [RegexHandler(
                '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
