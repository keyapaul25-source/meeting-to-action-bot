from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from meeting_bot.ai_analyzer import analyze_meeting
from meeting_bot.config import TELEGRAM_BOT_TOKEN
from meeting_bot.integrations.google_sheets import append_tasks_to_sheet
from meeting_bot.transcript_parser import parse_transcript


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Meeting-to-Action Bot. Send a transcript or a .txt file to analyze it."
    )


async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    parsed = parse_transcript(text)
    summary = analyze_meeting(parsed["clean"])

    response_lines = [
        "*Meeting Summary*",
        f"Overview: {summary.get('meeting_overview', 'No overview available.')}",
        "",
        "*Key Discussion Points*",
    ]

    for item in summary.get("key_discussion_points", []):
        response_lines.append(f"- {item}")

    response_lines.extend(["", "*Action Items*"])
    for item in summary.get("action_items", []):
        response_lines.append(
            f"- {item['task']} | Owner: {item['owner']} | Deadline: {item['deadline'] or 'Not specified'}"
        )

    if summary.get("missing_information"):
        response_lines.extend(["", "*Missing Information*"])
        for item in summary["missing_information"]:
            flags = []
            if item["missing_owner"]:
                flags.append("missing owner")
            if item["missing_deadline"]:
                flags.append("missing deadline")
            response_lines.append(f"- {item['task']}: {'; '.join(flags)}")

    await update.message.reply_text("\n".join(response_lines), parse_mode="Markdown")

    try:
        append_tasks_to_sheet(summary.get("action_items", []))
    except Exception:
        pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    if text:
        await analyze_text(update, context, text)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    doc = update.message.document
    if not doc:
        return
    if doc.mime_type not in {"text/plain", "application/octet-stream"}:
        await update.message.reply_text("Please upload a .txt file.")
        return

    file = await context.bot.get_file(doc.file_id)
    content = await file.download_as_bytearray()
    text = content.decode("utf-8", errors="ignore")
    await analyze_text(update, context, text)


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Create a .env file before running the bot.")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.TEXT, handle_document))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
