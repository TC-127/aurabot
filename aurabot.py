from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from collections import defaultdict
import asyncio

# Replace 'YOUR_TOKEN' with your bot's API token
TOKEN = '7040629306:AAEo3Ys0eNJ6zHDWdhJ8XSXwlNIotiW8NX4'

# In-memory storage for user points
user_points = defaultdict(int)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("reply to user with /aura x to change aura by x. /aurastats to see leaderboard.")

async def aura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract the points to be added or subtracted
        points = int(context.args[0])
        user_id = update.message.from_user.id

        # Update user points
        user_points[user_id] += points

        await update.message.reply_text(f"your aura is now {user_points[user_id]}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /aura <number> (where <number> is the amount of aura to add or subtract)")

async def aurastats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not user_points:
        await update.message.reply_text("No aura stats recorded yet.")
        return

    # Create a leaderboard string
    leaderboard = "Leaderboard:\n"
    for user_id, points in sorted(user_points.items(), key=lambda x: x[1], reverse=True):
        # Fetch user information
        member = await context.bot.get_chat_member(update.message.chat.id, user_id)
        user_name = member.user.full_name
        leaderboard += f"{user_name}: {points} aura\n"

    await update.message.reply_text(leaderboard)

async def main() -> None:
    # Create Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aura", aura))
    application.add_handler(CommandHandler("aurastats", aurastats))

    # Start the Bot
    await application.run_polling()