# What is this?

This is a minimalistic manager for you local backups of

- [Telegram chats exports](https://telegram.org/blog/export-and-more), through the Telegram's builtin export feature
- Telegram full backups through its Client SDK
- Slack full backups though its API

# What can it do?

Pretty much everything except sending messages:

- backup your chats and keep them up to date
- view your chats and messages
- display media content (images, videos, audio, files)

# How to use it?

## Telegram SDK

1. Create a new folder which will contain your Telegram backup. It is highly recommended to use an encrypted drive for
   this. I'll use the `/backups/telegram-sdk/` folder in this example.
2. Create a `.env` file in the `/backups/telegram-sdk/` folder with the following variables:
   `API_ID, API_HASH` - the credentials
   for [your Telegram app](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id), `PHONE` - the phone number
   associated with the Telegram account you want to back up. E.g.:
   ```shell
   API_ID=123456
   API_HASH=abcdef1234567890abcdef1234567890
   PHONE=+1234567890
   ```
3. Install the dependencies and run the backup script:
   ```shell
   cd backend
   pip install -r requirements.txt -r dev-requirements.txt
   python backup.py telegram-sdk /backups/telegram-sdk/
   ```
