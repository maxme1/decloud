export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.05a00956.js","app":"_app/immutable/entry/app.7c5e0906.js","imports":["_app/immutable/entry/start.05a00956.js","_app/immutable/chunks/entry.709cfef6.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/entry/app.7c5e0906.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
