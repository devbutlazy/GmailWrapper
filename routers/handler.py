import re
import email
import imaplib
import logging

from aiogram import Bot, Router
import traceback

# Initialize logging
logger = logging.getLogger("aiogram")

# Global variables
LAST_MESSAGE_ID = None

# Router instance
router = Router()


class MailHandler:
    def __init__(self) -> None:
        # Email configuration
        self.EMAIL = ""
        self.SMTP_PSWD = ""
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT = 993

    async def get_last_id(self) -> int:
        """
        Retrieves the ID of the last email in the inbox.
        """

        with imaplib.IMAP4_SSL(self.SMTP_SERVER) as mail:
            mail.login(self.EMAIL, self.SMTP_PSWD)
            mail.select("inbox")
            id_list = mail.search(None, "ALL")[1][0].split()

        return int(id_list[-1])

    async def app_main(self, bot: Bot, user_id: int) -> None:
        global LAST_MESSAGE_ID
        text = "🔔 *New Email*\n\n"

        mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
        mail.login(self.EMAIL, self.SMTP_PSWD)
        mail.select("inbox")

        try:
            data = mail.fetch(str(await self.get_last_id()), "(RFC822)")
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_bytes(arr[1])
                    email_from = re.sub(
                        r"[.=<>]", lambda x: "\\" + x.group(), msg["from"]
                    )
                    email_subject = msg["subject"]

                    text += f"*From:* {email_from}\n"
                    text += f"*Subject:* {email_subject}\n"

                    for part in msg.walk():
                        if part.is_multipart():
                            continue
                        content_type = part.get_content_type()
                        charset = part.get_param("charset", "utf-8")
                        if content_type == "text/plain":
                            body = re.sub(
                                r"=",
                                lambda x: "\\" + x.group(),
                                part.get_payload(decode=True).decode(charset),
                            )
                            text += f"*Content:*\n```...\n{body}```"

            await bot.send_message(chat_id=user_id, text=text)

        except BaseException:
            traceback.print_exc()

        # Update last message ID
        LAST_MESSAGE_ID = await self.get_last_id()


async def start_monitoring(bot: Bot, user_id: int) -> None:
    """
    Monitors email inbox for new messages and sends notifications to the user.
    """
    global LAST_MESSAGE_ID
    handler = MailHandler()

    logger = logging.getLogger("aiogram")
    logger.info("Successfully logged into Gmail")

    while True:
        try:
            # Initialize LAST_MESSAGE_ID if not set
            if LAST_MESSAGE_ID is None:
                LAST_MESSAGE_ID = await handler.get_last_id()

            # Check for new messages
            current_message_id = await handler.get_last_id()
            if LAST_MESSAGE_ID != current_message_id:
                await handler.app_main(bot, user_id)
                LAST_MESSAGE_ID = current_message_id

        except Exception as e:
            logger.error(f"An error occurred: {e}")
