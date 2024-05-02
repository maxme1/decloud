import type { Message, PhoneCall, EditChatTheme, InviteMembers, EditGroupPhoto, MigrateFromGroup, MigrateToSupergroup } from "./schema";

export type Service = PhoneCall | EditChatTheme | EditGroupPhoto | InviteMembers | MigrateFromGroup | MigrateToSupergroup;
export type AnyMessage = Message | Service;

function newGroup(present: AnyMessage, message: AnyMessage): boolean {
    if (present.type !== message.type) {
        return true;
    }
    if (present.type === 'service') {
        message = message as Service;
        if (present.actor_id !== message.actor_id) {
            return true;
        }
        if (present.action !== message.action) {
            return true;
        }
    } else {
        message = message as Message;
        if (present.from_id !== message.from_id) {
            return true;
        }
    }
    return false;
}

export function groupMessages(messages: AnyMessage[]): AnyMessage[][] {
    let result: AnyMessage[][] = [];
    let current: AnyMessage[] = [];
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

export { type Message };
