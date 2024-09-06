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
export function getAgent(entity: AgentMessage[] | string | null, info: ChatInfo): Agent | null {
    if (entity === null) return null;
    let uid: string | null;
    if (typeof entity === "string") {
        uid = entity;
    } else {
        uid = entity[0].agent_id;
    }
    if (uid == null) return null;
    const agent = info.agents.find((x) => x.id === uid);
    if (agent === undefined)
        console.log("Unknown agent: " + uid);
    return agent ?? null;
}

export function timeString(timestamp: string) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        hourCycle: "h24",
    });
}

import type { Agent, AgentMessage, AnyMessage, SystemMessage } from "./client";
import type { ChatInfo } from "$lib";

// TODO: remove this
type Message = AnyMessage;

export { type AgentMessage, type Message, type SystemMessage };
