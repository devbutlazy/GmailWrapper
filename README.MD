# Email Notification Bot

### This is a Python program that serves as a notification bot for monitoring new emails in your Gmail inbox and sending notifications via the Telegram messaging platform using the aiogram library.

## Features

    - Monitors Gmail inbox for new emails.
    - Sends notifications to a specified Telegram user whenever a new email is received.
    - Uses asyncio for asynchronous execution to minimize resource usage.
    - Handles errors gracefully and logs them for easy debugging.

## Installation

`1` Clone the repository:  
```
git ckone https://github.com/devbutlazy/GmailWrapper
```
`2` Install the required dependencies using pip:
```
pip install -r requirements.txt
```
`3` Next follow this:

    Set up your Gmail and Telegram Bot API credentials:

    Obtain Gmail credentials (email address and password).
    Create a new Telegram bot and obtain the API token.

    Update the EMAIL, SMTP_PSWD in the source/handler.py and TELEGRAM_API_TOKEN in the main.py variables with your credentials.

`4` Run the programm
```
python main.py
```

# What it does?
    The program starts monitoring your Gmail inbox for new emails.

    You'll receive notifications in your Telegram chat whenever a new email is received.

## Customization

    You can customize the notification messages and frequency of monitoring by modifying the code in app_main and start_monitoring functions in main.py.
    Adjust logging settings in logging.basicConfig() to change log levels or output format.


## License: GNU GPL 3
