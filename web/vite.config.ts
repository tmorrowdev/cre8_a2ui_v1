import {defineConfig} from 'vite';

// A2UI_API points the dev proxy at another agent server (default: the local one on 8000).
const api = process.env.A2UI_API ?? 'http://127.0.0.1:8000';

export default defineConfig({
  server: {
    port: 5173,
    proxy: {'/api': api},
  },
});
