

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/2.afb8159d.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js","_app/immutable/chunks/stores.710c1f89.js","_app/immutable/chunks/entry.79f13f35.js"];
export const stylesheets = ["_app/immutable/assets/2.33055757.css"];
export const fonts = [];
