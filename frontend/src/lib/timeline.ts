import type { PhoneCall, EditChatTheme, InviteMembers, EditGroupPhoto, MigrateFromGroup, MigrateToSupergroup } from "./schema";

export type Service = PhoneCall | EditChatTheme | EditGroupPhoto | InviteMembers | MigrateFromGroup | MigrateToSupergroup;
// export type Message = Message | Service;

function newGroup(present: Message, message: Message): boolean {
    if (present.type !== message.type) {
        return true;
    }
    if (present.type === 'system') {
        message = message as SystemMessage;
        return present.event != message.event;
        // message = message as SystemMessage;
        // if (present.actor_id !== message.actor_id) {
        //     return true;
        // }
        // if (present.action !== message.action) {
        //     return true;
        // }
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


export function isAgent(group: Message[]): group is AgentMessage[] {
    return group[0].type === "agent";
}
export function isSystem(group: Message[]): group is SystemMessage[] {
    return group[0].type === "system";
}
export function getAgent(group: AgentMessage[], info: ChatInfo): Agent | null {
    if (group[0].agent_id == null) return null;
    const agent = info.agents.find((x) => x.id == group[0].agent_id);
    if (agent === undefined)
        console.log("Unknown agent: " + group[0].agent_id);
    return agent ?? null;
}

import type { Agent, AgentMessage, SystemMessage } from "./client";
import type { ChatInfo } from "$lib";

type Message = AgentMessage | SystemMessage;

export { type AgentMessage, type Message, type SystemMessage };
