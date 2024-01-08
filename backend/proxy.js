const server = polka();

import { createProxyMiddleware } from 'http-proxy-middleware';

// Define the proxy middleware
const apiProxy = createProxyMiddleware('/api', {
	target: 'http://vish.vm.tornadovps.net:8080/', // Replace with your API server URL
	changeOrigin: true,
	pathRewrite: {
		'^/api': '', // Remove '/api' prefix
	},
});
server.use('/api', apiProxy);
  
server.use(handler);