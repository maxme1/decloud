# What is this?

This is a minimalistic browser of your local [backups of Telegram chats](https://telegram.org/blog/export-and-more).

A live version is available [here]().

# What can it do?

Pretty much everything except sending messages:

- view your chats and messages
- filter messages by text and content type (media, message types, authors etc.)
- display media content (images, videos, audio, files)
- show additional statistics, such as monthly/weekly/daily activity charts

# How to use it?

1. Export your chats from Telegram. See [this guide](https://telegram.org/blog/export-and-more) for details. If your
   chats contain sensitive information, make sure to keep the exported data in a secure location, such as an encrypted
   drive.
2. The backups will need a bit of processing. Choose a storage folder for the processed chats. Mine
   is `path/to/storage/folder`.
3. Run
   ```shell
   python normalizer/main.py path/to/storage/folder path/to/exported/chat/folder
   ```
   for each chat you backed up
4. Run the file server
   ```shell
   cd path/to/storage/folder 
   npx serve --cors
   ```
5. Run the frontend
   ```shell
   cd frontend
   npm install
   npm run dev
   ```   
6. Go to `localhost:5173` in your browser

It's not the most user-friendly setup. I hope to simplify it in the future.
