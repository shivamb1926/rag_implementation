import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from src.pipeline import ask

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TG_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    
    # Call your RAG pipeline
    result = ask(user_query)
    
    answer = result["answer"]
    sources = ", ".join(result["sources"])
    
    reply = f"{answer}\n\nSources: {sources}"
    
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()