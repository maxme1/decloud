

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.f7f4b95b.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js","_app/immutable/chunks/stores.710c1f89.js","_app/immutable/chunks/entry.79f13f35.js"];
export const stylesheets = [];
export const fonts = [];
