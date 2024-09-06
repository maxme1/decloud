// place files you want to import through the `$lib` alias in this folder.

import type { Agent, Chat, ChatInfo as _ChatInfo } from "./client";
// import { emojis } from "./emojis.json";



interface ChatInfo extends _ChatInfo {
    channels: Array<Chat>;
}

let filesRoot = import.meta.env.VITE_FILE_SERVER ?? "http://localhost:3000/";
// let standardEmojis = new Map<string, string>(emojis.map((e) => [e.shortname.slice(1, e.shortname.length - 1), e.emoji]));

export { filesRoot, type ChatInfo };
