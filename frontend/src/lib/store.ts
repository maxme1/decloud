import { writable, type Writable } from 'svelte/store';
import type { Chat } from './client';

export const activeChannel = writable(null);
export const channels: Writable<Chat[]> = writable([]);
