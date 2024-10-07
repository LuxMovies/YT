import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes

TOKEN = os.environ.get('TELEGRAM_TOKEN')

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the YouTube Live Stream Downloader bot! Send me a YouTube live stream URL to download it.")

def download_stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    try:
        # Get the stream object
        streams = pytube.YouTube(url).streams.filter(only_audio=False)

        # Get the highest quality stream
        highest_quality_stream = streams.order_by('resolution').desc().first()

        # Get the stream URL
        stream_url = highest_quality_stream.url

        # Get the stream quality
        stream_quality = highest_quality_stream.resolution

        # Get the stream length
        stream_length = highest_quality_stream.length

        # Get the total size of the stream
        total_size = highest_quality_stream.filesize

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Stream URL: {stream_url}\nStream Quality: {stream_quality}\nStream Length: {stream_length} seconds\nTotal Size: {total_size} bytes")

        # Ask the user if they want to download the stream
        context.bot.send_message(chat_id=update.effective_chat.id, text="Do you want to download the stream? (yes/no)")

        def download(update, context):
            if update.message.text.lower() == "yes":
                # Download the stream using streamlink
                stream = streamlink.streams(stream_url)
                streamlink.streams(stream_url)["best"].dump_to_file("output.mp4")
                context.bot.send_message(chat_id=update.effective_chat.id, text="Download complete!")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Download cancelled.")

        context.bot.send_message(chat_id=update.effective_chat.id, text="Please respond with 'yes' or 'no'")

        return download

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error: " + str(e))

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    download_stream_handler = MessageHandler(None, download_stream)
    application.add_handler(download_stream_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
