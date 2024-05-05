export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["chats/chats.json","chats/user1.json"]),
	mimeTypes: {".json":"application/json"},
	_: {
		client: {"start":"_app/immutable/entry/start.75bcf8e2.js","app":"_app/immutable/entry/app.d889f7a8.js","imports":["_app/immutable/entry/start.75bcf8e2.js","_app/immutable/chunks/entry.79f13f35.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/entry/app.d889f7a8.js","_app/immutable/chunks/scheduler.3fa178e2.js","_app/immutable/chunks/index.e4b3e33d.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
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
