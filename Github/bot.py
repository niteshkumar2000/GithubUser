#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


import logging
import subprocess
import os
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = 'YOUR_BOT_TOKEN_HERE'

def start(update, context):
    update.message.reply_text('Hello! I\'m Github userinfo bot. Use /help')


def help(update, context):
    update.message.reply_text('Give me a valid github username, I\'ll tell about the user\'s github profile :)')


def echo(update, context):
    print(update.message.text)
   
    p = subprocess.Popen(f'scrapy crawl GitUser -a username={update.message.text} -o user.json')
    p.wait()

    with open('user.json') as f:
        data = json.load(f)[0]
    
    with open('user.json', 'w') as outfile:
        json.dump(data, outfile)

    with open('user.json') as f:
        data = json.load(f)

    subprocess.Popen('rm user.json')

    text = '==========User Info==========\n\n'

    for key in data:
        if key == 'Pinned':
            text += '\n==========User Info==========\n'
            text += '\n==========Pinned Repos==========\n\n'
            for repo in data[key]:
                for item in data[key][repo]:
                    if data[key][repo][item] is None:
                        data[key][repo][item] = 'None'
                    text += item + ': ' + data[key][repo][item] + '\n'
                text += '\n'
        else:
            if data[key] is None:
                data[key] = 'None'
            text += key + ': ' + data[key].replace('\n', '') + '\n'

    text += '==========Pinned Repos=========='

    update.message.reply_text(text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
