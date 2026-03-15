import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import { queryClient } from './app/providers/query-client'
import { App } from './app/App'
import { enableMocking } from './shared/mocks/browser'
import './index.css'

async function bootstrap() {
  if (import.meta.env.DEV) {
    await enableMocking()
  }

  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    </StrictMode>,
  )
}

void bootstrap()
