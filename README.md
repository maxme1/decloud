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

# How do I backup my chats?

## Slack

1. Create a new folder which will contain your Slack backup. It is highly recommended to use an encrypted drive for
   this. I'll use the `/backups/slack/` folder in this example.
2. Create a `.env` file in the `/backups/slack/` folder with your [Slack API token](https://api.slack.com/apps). E.g.:
   ```shell
   TOKEN=xoxb-mytoken
   ```
3. Install the dependencies and run the backup script:
   ```shell
   cd backend
   pip install -r requirements.txt -r dev-requirements.txt
   python backup.py slack /backups/slack/
   ```

## Telegram SDK

1. Create a new folder which will contain your Telegram backup. It is highly recommended to use an encrypted drive for
   this. I'll use the `/backups/telegram-sdk/` folder in this example.
2. Create a `.env` file in the `/backups/telegram-sdk/` folder with the following variables:
   `API_ID, API_HASH` - the credentials
   for [your Telegram app](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id), `PHONE` - the phone number
   associated with the Telegram account you want to back up, `ENCRYPTION_KEY` - a key used to encrypt you local telegram
   database (required by tdlib). E.g.:
   ```shell
   API_ID=123456
   API_HASH=abcdef1234567890abcdef1234567890
   PHONE=+1234567890
   ENCRYPTION_KEY=MAKE_SURE_YOUR_ENCRYPTION_KEY_IS_STRONG_AND_SECURE
   ```
3. Install the dependencies and run the backup script:
   ```shell
   cd backend
   pip install -r requirements.txt -r dev-requirements.txt
   python backup.py telegram-sdk /backups/telegram-sdk/
   ```

# How do I view my chats?

## Start the backend

1. Enter the `backend` folder:
   ```shell
   cd backend
   ```
2. Create a `.env` file with the following variables. Note that you have to supply the correct paths to the backups you
   want to view. E.g.:
   ```shell
   BASE_URL=http://localhost:9000
   SLACK=/backups/slack/ # only if you have a Slack backup
   TELEGRAM_SDK=/backups/telegram-sdk/ # only if you have a Telegram SDK backup
   TELEGRAM_EXPORT=/backups/telegram-export/ # only if you have a Telegram export backup
   ```
3. Download the assets:
   ```shell
   ./download-assets.sh
   ```
4. Install the dependencies:
   ```shell
   pip install -r requirements.txt
   ```
5. Start the backend:
   ```shell
   uvicorn src.app:app --port 9000 --reload 
   ```

Note that the steps 1-4 are only required the first time.

## Start the frontend

1. Enter the `frontend` folder:
   ```shell
   cd frontend
   ```
2. Install the dependencies:
   ```shell
   npm install
   ```
3. Generate the client:
   ```shell
   npm run generate-client
   ```
4. Start the frontend:
   ```shell
   npm run dev
   ```

The steps 1-3 are only required the first time.

## Enjoy

Go to `http://localhost:5173/`. That's it!
