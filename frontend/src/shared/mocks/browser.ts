export async function enableMocking() {
  const { worker } = await import('./worker')
  await worker.start({
    onUnhandledRequest: 'bypass',
  })
}
