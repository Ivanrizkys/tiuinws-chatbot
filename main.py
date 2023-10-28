import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# conversation mode
FIRST_STATE = range(1)

async def start_add_question_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tolong masukkan request pertanyaan yang akan ditambahkan ke dalam chatbot")
    return FIRST_STATE

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    await update.message.reply_text(f"Pertanyaan yang sudah anda masukkan kedalam database adalah \n\n{user_response}")
    await update.message.reply_text("Terimakasih semoga feedback yang anda berikan dapat membuat chatbot lebih baik lagi kedepanya :)")
    return ConversationHandler.END

async def cancel_add_question_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Proses dibatalkan")
    return ConversationHandler.END


# default mode
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("last name sender", update.message.chat.last_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hai sayang :)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6320237733:AAG_xry4Hsj9lhCXZ4gazEa_wt_8UzCrN_s').build()
    
    # conversation handler
    add_mode_handler = ConversationHandler(
        entry_points=[CommandHandler("add", start_add_question_mode)],
        states={
            FIRST_STATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), add_question)],
        },
        fallbacks=[CommandHandler("cancel_add", cancel_add_question_mode)]
    )
    
    # handler
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # register handler
    application.add_handler(start_handler)
    application.add_handler(add_mode_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()