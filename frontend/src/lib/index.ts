import { type Agent, type Chat, type ChatInfo as _ChatInfo, DefaultService as ApiService, OpenAPI } from "./client";

OpenAPI.BASE = "http://localhost:9000";

interface ChatInfo extends _ChatInfo {
    channels: Array<Chat>;
}


export { type ChatInfo, ApiService };
