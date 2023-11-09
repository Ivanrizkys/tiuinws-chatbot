import chat
import config

import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#* conversation mode
FIRST_STATE = range(1)
async def start_add_question_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(chat.REQUEST_QUESTION)
    return FIRST_STATE

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text

    req_data = {
        'data': {
            'question': user_response
        }
    }
    res = requests.post(f'{config.SERVER_URL}/questions', json=req_data, headers=config.HEADERS)
    if res.status_code != 200:
        await update.message.reply_text(chat.ERROR_ADD_QUESTION)
    else:
        await update.message.reply_html(f"{chat.REQUEST_QUESTION_RESULT} \n\n<b>{user_response}</b>")
        await update.message.reply_text(chat.THANKS_FOR_FEEDBACK)
    return ConversationHandler.END

async def cancel_add_question_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(chat.CANCEL_REQUEST_QUESTION)
    return ConversationHandler.END


#* default mode
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("last name sender", update.message.chat.last_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chat.START, parse_mode='HTML')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="", parse_mode='HTML')

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.CHATBOT_TOKEN).build()
    
    # conversation handler
    add_mode_handler = ConversationHandler(
        entry_points=[CommandHandler("add", start_add_question_mode)],
        states={
            FIRST_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), add_question)],
        },
        fallbacks=[CommandHandler("cancel", cancel_add_question_mode)]
    )
    
    #* handler
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    #* register handler
    application.add_handler(start_handler)
    application.add_handler(add_mode_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()