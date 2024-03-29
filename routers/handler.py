import email
import imaplib
import logging

from aiogram import Bot, Router
import traceback

# Initialize logging
logger = logging.getLogger("aiogram")

# Global variables
LAST_MESSAGE_ID = None

# Email configuration
EMAIL = ""
SMTP_PSWD = ""
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

# Router instance
router = Router()


async def get_last_id() -> int:
    """
    Retrieves the ID of the last email in the inbox.
    """
    try:
        with imaplib.IMAP4_SSL(SMTP_SERVER) as mail:
            mail.login(EMAIL, SMTP_PSWD)
            mail.select("inbox")
            _, data = mail.search(None, "ALL")
            mail_ids = data[1]
            id_list = mail_ids[0].split()

            if id_list:
                return int(id_list[-1])
            else:
                return 0  # Return 0 if there are no emails in the inbox

    except BaseException as e:
        logger.error(f"Error occurred while fetching last email ID: {e}")
        return -1  # Return -1 to indicate an error occurred


async def app_main(bot: Bot, user_id: int) -> None:
    global LAST_MESSAGE_ID
    text = "🔔 *New Email*\n\n"

    try:
        # Connect to the email server
        with imaplib.IMAP4_SSL(SMTP_SERVER) as mail:
            mail.login(EMAIL, SMTP_PSWD)
            mail.select("inbox")

            # Retrieve all emails
            _, data = mail.search(None, "ALL")

            # Process each email
            for num in data[0].split():
                _, response = mail.fetch(num, "(RFC822)")
                _, arr = response[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_bytes(arr)
                    email_from = msg["from"]
                    email_subject = msg["subject"]

                    # Prepare email content for notification
                    escaped_email_from = email_from.replace('.', '\.').replace("=", "\=")
                    text += f"*From:* {escaped_email_from.replace('<', '').replace('>', '')}\n"
                    text += f"*Subject:* {email_subject}\n"

                    # Extract email body
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_param("charset", "utf-8")  # Default to UTF-8
                            body = part.get_payload(decode=True).decode(charset).replace("=", "\=")
                            text += f"*Content:*\n```...\n{body}```"
                            break  # Only consider the first plain text part

        # Send notification
        await bot.send_message(chat_id=user_id, text=text)

    except Exception:
        traceback.print_exc()

    # Update last message ID
    LAST_MESSAGE_ID = await get_last_id()


async def start_monitoring(bot: Bot, user_id: int) -> None:
    """
    Monitors email inbox for new messages and sends notifications to the user.
    """
    global LAST_MESSAGE_ID

    logger = logging.getLogger("aiogram")
    logger.info("Successfully logged into Gmail")

    while True:
        try:
            # Initialize LAST_MESSAGE_ID if not set
            if LAST_MESSAGE_ID is None:
                LAST_MESSAGE_ID = await get_last_id()

            # Check for new messages
            current_message_id = await get_last_id()
            if LAST_MESSAGE_ID != current_message_id:
                await app_main(bot, user_id)
                LAST_MESSAGE_ID = current_message_id

        except Exception as e:
            logger.error(f"An error occurred: {e}")
