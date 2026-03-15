import { useQuery } from '@tanstack/react-query'
import { Activity, Database, HeartPulse } from 'lucide-react'
import { useSelectedArticle } from '../../features/article-picker/model/use-selected-article'
import { http } from '../../shared/api/http'
import { Badge } from '../../shared/ui/badge'
import { Card } from '../../shared/ui/card'

export function ActivityOverview() {
  const { selectedArticleId } = useSelectedArticle()
  const { data: health, isLoading, isError } = useQuery({
    queryKey: ['api-health'],
    queryFn: async () => {
      const { data } = await http.get<{ status: string; message: string }>('/health')
      return data
    },
  })

  if (isLoading) {
    return <Card>Проверяю доступность API...</Card>
  }

  if (isError || !health) {
    return <Card>API недоступен. Проверьте запуск backend на `localhost:8000`.</Card>
  }

  return (
    <div className="space-y-5">
      <Card>
        <div className="flex items-center gap-2">
          <HeartPulse className="h-4 w-4 text-muted" />
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Статус backend</p>
        </div>
        <h2 className="mt-2 text-2xl text-ink">Подключение активно</h2>
        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-1">
          <Metric label="Health" value={health.status} />
          <Metric label="Message" value={health.message} />
          <Metric label="Base URL" value="/api/v1" />
          <Metric label="Текущий arXiv ID" value={selectedArticleId || 'не выбран'} />
        </div>
      </Card>

      <Card>
        <div className="flex items-end justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <Database className="h-4 w-4 text-muted" />
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Ограничения API</p>
            </div>
            <h2 className="mt-2 text-2xl text-ink">Что реально доступно</h2>
          </div>
          <Badge>live backend</Badge>
        </div>
        <div className="mt-5 space-y-3 text-sm text-muted">
          <p>Поиск статей работает через `articles/search`.</p>
          <p>После выбора статья сохраняется через `articles/download` и получает UUID.</p>
          <p>Оценка и обзор вызываются реальными эндпоинтами `evaluations/evaluate` и `reviews/write`.</p>
        </div>
      </Card>

      <Card>
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-muted" />
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Что отключено</p>
        </div>
        <h2 className="mt-2 text-2xl text-ink">Моки больше не нужны</h2>
        <div className="mt-4 space-y-3 text-sm text-muted">
          <p>Фронт больше не использует MSW и не стучится в `/api/history` или `/api/analytics`.</p>
          <p>Квиз и рекомендации временно скрыты как отдельные backend-фичи, потому что для них нет маршрутов в FastAPI.</p>
        </div>
      </Card>
    </div>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[22px] border border-line bg-paper/80 p-4">
      <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">{label}</p>
      <p className="mt-2 text-3xl text-ink">{value}</p>
    </div>
  )
}
