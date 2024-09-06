import { writable, type Writable } from 'svelte/store';
import type { AnyMessage, Chat } from './client';
import type { ChatInfo } from '$lib';

export interface ActiveChannel {
    channel: Chat;
    messages: AnyMessage[];
    info: ChatInfo;
}

export const activeChannel: Writable<ActiveChannel | null> = writable(null);
export const channels: Writable<Chat[]> = writable([]);
