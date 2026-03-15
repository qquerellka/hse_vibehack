import { ActivityOverview } from '../activity-overview/ActivityOverview'
import { ArticleHub } from '../article-hub/ArticleHub'
import { ArticleSearch } from '../../features/article-search/ui/ArticleSearch'

export function AppShell() {
  return (
    <main className="mx-auto min-h-screen max-w-[1600px] px-4 py-6 md:px-6 lg:px-8">
      <section className="mb-6 rounded-[36px] border border-line bg-white/70 p-6 shadow-panel backdrop-blur-sm">
        <p className="font-mono text-xs uppercase tracking-[0.32em] text-muted">Science Helpy</p>
        <div className="mt-4 grid gap-5 lg:grid-cols-[1.2fr,0.8fr]">
          <div>
            <h1 className="max-w-4xl text-5xl leading-[0.96] text-ink md:text-7xl">
              Преврати пайплайн агентов в понятный и удобный продукт.
            </h1>
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[360px,minmax(0,1fr),340px]">
        <ArticleSearch />
        <ArticleHub />
        <ActivityOverview />
      </section>
    </main>
  )
}
