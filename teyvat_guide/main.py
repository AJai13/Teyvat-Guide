# fazer uma calculadora geral
    #3 comando = 1. weapon, 2. artifacts, 3. geral (todos)

# pip install -e .

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, filters
from teyvat_guide.calculator import character_calculator
from teyvat_guide.daily_reward import reward_info, claimed_rewards, claim_daily_reward



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
) # 28/11/2022 15:00:00 - adam - INFO - oi oi

logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start)) # /start
    # dispatcher.add_handler(CommandHandler("help", help_command)) # /help
    dispatcher.add_handler(CommandHandler("reward", reward_info)) # /reward
    dispatcher.add_handler(CommandHandler("claimed", claimed_rewards)) # /claimed rewards
    dispatcher.add_handler(CommandHandler("claim", claim_daily_reward)) # /claim daily rewards
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, character_calculator)) # character's name
    #weapon
    #artifacts


    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, echo)) # echo

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
