import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)

from src.pipeline import ask

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TG_TOKEN")

async def process_query(update: Update, query: str):
    result = ask(query)

    answer = result["answer"]
    sources = ", ".join(result["sources"])

    reply = f"{answer}\n\nSources: {sources}"
    await update.message.reply_text(reply)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    await process_query(update, user_query)

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ask <your query>")
        return

    query = " ".join(context.args)
    await process_query(update, query)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Commands:
/ask <query> - Ask a question using the RAG system
/help - Show this help message

You can also just type your question directly without using /ask.
"""
    await update.message.reply_text(help_text)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("help", help_command))
    
    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()