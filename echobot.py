#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
import screener as sc
import functions as f
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    name = update.message.chat.first_name
    update.message.reply_text(f'{name}! Welcome to Stocks Alerts! Send Alert for get Stocks Alerts')

def alert(update, context):
    stocks = sc.initBot()
    update.message.reply_text("ALERTS FOR CHECK")
    for stock in stocks:
        update.message.reply_text(stock.upper())

def help_command(update, context):
    update.message.reply_text('Send /Alert and you get Alert Stocks')

def echo(update, context):
    ticker = update.message.text.lower()
    messageAlert = sc.initOneStock(ticker)
    update.message.reply_text("PRICE CLOSE")
    update.message.reply_text(round(messageAlert[4], 2))

def main():
    updater = Updater("ADDTOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("alert", alert))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()