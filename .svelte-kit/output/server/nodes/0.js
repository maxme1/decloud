

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.f6e546d0.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js"];
export const stylesheets = ["_app/immutable/assets/0.26e40c7b.css"];
export const fonts = [];
