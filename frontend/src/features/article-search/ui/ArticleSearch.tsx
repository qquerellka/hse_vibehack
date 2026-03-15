import { startTransition, useDeferredValue, useState } from 'react'
import { Search } from 'lucide-react'
import { useArticles } from '../../../entities/article/api/article-api'
import { useSelectedArticle } from '../../article-picker/model/use-selected-article'
import { Badge } from '../../../shared/ui/badge'
import { Card } from '../../../shared/ui/card'
import { Button } from '../../../shared/ui/button'

export function ArticleSearch() {
  const { selectedArticleId, setSelectedArticleId, searchTerm, setSearchTerm } = useSelectedArticle()
  const [draft, setDraft] = useState(searchTerm)
  const deferredSearch = useDeferredValue(searchTerm)
  const { data: articles = [], isLoading } = useArticles(deferredSearch)

  return (
    <Card className="space-y-4">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Поиск статей</p>
          <h2 className="mt-2 text-2xl text-ink">Входящий поток</h2>
        </div>
        <Badge>Найдено: {articles.length}</Badge>
      </div>

      <label className="flex items-center gap-3 rounded-full border border-line bg-paper px-4 py-3">
        <Search className="h-4 w-4 text-muted" />
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Ищи агентов, инференс, retrieval..."
          className="w-full border-0 bg-transparent text-sm outline-none placeholder:text-muted"
        />
        <Button
          type="button"
          onClick={() => {
            startTransition(() => {
              setSearchTerm(draft)
            })
          }}
          className="px-3 py-1.5 text-xs"
        >
          Найти
        </Button>
      </label>

      <div className="space-y-3">
        {isLoading && <p className="text-sm text-muted">Загружаю результаты поиска...</p>}
        {articles.map((article) => (
          <button
            key={article.id}
            type="button"
            onClick={() => {
              startTransition(() => {
                setSelectedArticleId(article.id)
              })
            }}
            className={`w-full rounded-[22px] border p-4 text-left transition-all ${
              selectedArticleId === article.id
                ? 'border-ink bg-ink text-paper'
                : 'border-line bg-white/50 text-ink hover:-translate-y-0.5 hover:border-ink'
            }`}
          >
            <div className="flex items-center justify-between gap-3">
              <span className="font-mono text-xs uppercase tracking-[0.22em]">
                {article.id}
              </span>
              <span className="text-xs">{article.published}</span>
            </div>
            <h3 className="mt-3 text-lg leading-tight">{article.title}</h3>
            <p className={`mt-2 line-clamp-3 text-sm ${selectedArticleId === article.id ? 'text-paper/80' : 'text-muted'}`}>
              {article.abstract}
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {article.tags.map((tag) => (
                <Badge key={tag} className={selectedArticleId === article.id ? 'border-white/20 bg-white/10 text-paper/80' : ''}>
                  {tag}
                </Badge>
              ))}
            </div>
          </button>
        ))}
      </div>
    </Card>
  )
}
