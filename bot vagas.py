#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
import os
from os.path import join, dirname
from dotenv import load_dotenv
import mysql.connector

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Conexao ao BD
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vaga_bot"
    )


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def minerar(context: CallbackContext) -> None:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    URL = 'https://github.com/frontendbr/vagas/issues'

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    tags = []
    for vaga in soup.findAll('div', attrs={'class': 'd-flex Box-row--drag-hide position-relative'}):
        tags.clear()
        tags_texto = ''
        link = ''
        texto = ''
        tags_texto
        texto += f"Título: {vaga.find('a', attrs={'class', 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'}).string}\n\n"
        link = vaga.find('a', attrs={'class',
                                     'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})[
            'href']

        ID = vaga.find('span', attrs={'class', 'opened-by'})

        # ID.text.strip()[ID.text.strip().index('#') + 1:ID.text.strip().index(' ') + 1]

        indice = int(ID.text.strip()[ID.text.strip().index('#') + 1:ID.text.strip().index(' ') + 1])

        tags = vaga.findAll('span', attrs={'class', 'labels lh-default d-block d-md-inline'})
        for tag in tags:
            for text_tag in tag.strings:
                tags_texto += f'{text_tag.strip()} '
            # tags_texto += f'{tag.text} - '
        texto += f"Tags: {tags_texto.strip().replace('  ', ' ').replace(' ', ', ')}\n"
        texto.rfind(',')
        # print(f'https://www.github.com{link}')

        page = requests.get(f'https://www.github.com{link}', headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')

        texto += f"{soup.find('td', attrs={'class', 'd-block'}).text}"

        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT IDvaga FROM vaga order by ID DESC")

        myresult = mycursor.fetchone()

        mycursor.close()

        job = context.job
        if myresult:
            if myresult[0] != indice:
                context.bot.send_message(job.context, text=texto)

                mycursor = mydb.cursor()

                sql = "INSERT INTO vaga (IDvaga) VALUES (%s)"
                val = (indice, )

                mycursor.execute(sql, val)

                mydb.commit()
            else:
                context.bot.send_message(job.context, text="Já adicionado")

            # job = context.job
            # context.bot.send_message(job.context, text=f'{myresult[0]}-{indice}')
        #         if x[0] == update.message.chat_id:
        #             return True
        # return False

        # update.message.reply_text(texto)

        break


# def alarm(context: CallbackContext) -> None:
#     """Send the alarm message."""
#     job = context.job
#     context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# def set_timer(update: Update, context: CallbackContext) -> None:
#     """Add a job to the queue."""
#     chat_id = update.message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         due = int(context.args[0])
#         if due < 0:
#             update.message.reply_text('Sorry we can not go back to future!')
#             return
#
#         job_removed = remove_job_if_exists(str(chat_id), context)
#         context.job_queue.run_repeating(minerar, 5, context=chat_id, name=str(chat_id))
#
#         text = 'Timer successfully set!'
#         if job_removed:
#             text += ' Old one was removed.'
#         update.message.reply_text(text)
#
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /set <seconds>')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('Hi!')
    """Add a job to the queue."""
    chat_id = update.message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(minerar, 2, context=chat_id, name=str(chat_id))

    text = 'Bot ativado com sucesso'
    if job_removed:
        text += ' Old one was removed.'
    update.message.reply_text(text)





def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the \command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(), title="Caps", input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)), parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)), parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)


# Função principal
def main() -> None:

    # Guardando o token do bot
    dotenv_path = join(dirname(__file__), '.env')

    # Carregando o token
    load_dotenv(dotenv_path)

    # Adicionando o token ao carregador do bot
    updater = Updater(os.environ.get("token"))

    # Registrador de solicitações do usuário
    dispatcher = updater.dispatcher

    # Comando do usuário, /start
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Para mensagens que não são comandos
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Starta o bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()