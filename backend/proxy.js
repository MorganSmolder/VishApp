const server = polka();

import { createProxyMiddleware } from 'http-proxy-middleware';

// Define the proxy middleware
const apiProxy = createProxyMiddleware('/api', {
	target: 'http://127.0.0.1:8080/', 
	changeOrigin: true,
	logLevel: "debug",
	pathRewrite: {
		'^/api': '', // Remove '/api' prefix
	},
	headers: {
		"Connection": "keep-alive"
	},
});
server.use('/api', apiProxy);

server.use(handler);

server.listen({ path, host, port }, () => {
	console.log(`Listening on ${path ? path : host + ':' + port}`);
});

export { host, path, port, server };
