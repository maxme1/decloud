

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/2.f81f045a.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js","_app/immutable/chunks/stores.d56c4fdd.js","_app/immutable/chunks/entry.709cfef6.js"];
export const stylesheets = ["_app/immutable/assets/2.33055757.css"];
export const fonts = [];
