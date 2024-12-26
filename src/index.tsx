import { Hono } from 'hono'
import type { FC } from 'hono/jsx'
import { serveStatic } from '@hono/node-server/serve-static'

const app = new Hono()

const Layout: FC = (props) => {
  return (
    <html lang='en'>
      <body>{props.children}</body>
    </html>
  )
}

const Top: FC<{ messages: string[] }> = (props: {
  messages: string[]
}) => {
  return (
    <Layout>
      <h1>Hello Hono!</h1>
      <ul>
        {props.messages.map((message) => {
          return <li key={message}>{message}!!</li>
        })}
      </ul>
    </Layout>
  )
}

app.get('/', (c) => {
  const messages = ['Good Morning', 'Good Evening', 'Good Night']
  return c.html(<Top messages={messages} />)
})

app.use('/static/*', serveStatic({ root: './' }))

export default app
