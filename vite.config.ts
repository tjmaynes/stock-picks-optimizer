import { defineConfig } from 'vite'
import build from '@hono/vite-build/node'
import devServer from '@hono/vite-dev-server'

const port = 3000

export default defineConfig({
  plugins: [
    build({
      entry: './src/index.tsx',
      port: port,
      entryContentBeforeHooks: [
        () => `console.log("Server running on port ${port}...");`,
      ],
    }),
    devServer({
      entry: 'src/index.tsx',
    }),
  ],
})
