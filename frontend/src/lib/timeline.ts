import type { PhoneCall, EditChatTheme, InviteMembers, EditGroupPhoto, MigrateFromGroup, MigrateToSupergroup } from "./schema";

export type Service = PhoneCall | EditChatTheme | EditGroupPhoto | InviteMembers | MigrateFromGroup | MigrateToSupergroup;
// export type Message = Message | Service;

function newGroup(present: Message, message: Message): boolean {
    if (present.type !== message.type) {
        return true;
    }
    if (present.type === 'system') {
        return false;
        message = message as SystemMessage;
        if (present.actor_id !== message.actor_id) {
            return true;
        }
        if (present.action !== message.action) {
            return true;
        }
    } else {
        message = message as AgentMessage;
        if (present.agent_id === null || message.agent_id === null) {
            return true;
        }
        if (present.agent_id !== message.agent_id) {
            return true;
        }
    }
    return false;
}

export function groupMessages(messages: Message[]): Message[][] {
    let result: Message[][] = [];
    let current: Message[] = [];
    for (const message of messages) {
        if (current.length === 0) {
            current.push(message);
            continue;
        }
        if (newGroup(current[0], message)) {
            result.push(current);
            current = [message];
        } else {
            current.push(message);
        }
    }
    if (current.length > 0) {
        result.push(current);
    }
    return result
}

import type { AgentMessage, SystemMessage } from "./client";

type Message = AgentMessage | SystemMessage;

export { type AgentMessage, type Message, type SystemMessage };
