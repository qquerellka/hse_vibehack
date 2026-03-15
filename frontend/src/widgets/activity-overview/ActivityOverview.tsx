import { useAnalytics } from '../../entities/analytics/api/analytics-api'
import { useHistory } from '../../entities/session/api/session-api'
import { Badge } from '../../shared/ui/badge'
import { Card } from '../../shared/ui/card'
import { Meter } from '../../shared/ui/meter'

function formatStatus(status: string) {
  if (status === 'mastered') return 'изучено'
  if (status === 'reviewed') return 'разобрано'
  if (status === 'reading') return 'в процессе'
  if (status === 'queued') return 'в очереди'
  return status
}

function activityTone(count: number) {
  if (count === 0) return 'bg-white'
  if (count === 1) return 'bg-[#dbd4c7]'
  if (count === 2) return 'bg-[#b7ae9d]'
  if (count === 3) return 'bg-[#736b60]'
  return 'bg-ink'
}

export function ActivityOverview() {
  const { data: analytics } = useAnalytics()
  const { data: history = [] } = useHistory()

  if (!analytics) {
    return <Card>Загружаю аналитику...</Card>
  }

  return (
    <div className="space-y-5">
      <Card>
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Аналитика обучения</p>
        <h2 className="mt-2 text-2xl text-ink">Память прогресса</h2>
        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-1">
          <Metric label="Статей прочитано" value={analytics.totalRead.toString()} />
          <Metric label="Разобрано глубоко" value={analytics.totalReviewed.toString()} />
          <Metric label="Точность квизов" value={`${analytics.quizAccuracy}%`} />
          <Metric label="Серия" value={`${analytics.streak} дней`} />
        </div>
      </Card>

      <Card>
        <div className="flex items-end justify-between gap-3">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Календарь активности</p>
            <h2 className="mt-2 text-2xl text-ink">Ритм чтения</h2>
          </div>
          <Badge>стиль GitHub</Badge>
        </div>
        <div className="mt-5 grid grid-cols-5 gap-2 sm:grid-cols-10">
          {analytics.activity.map((day) => (
            <div key={day.date} className="space-y-1">
              <div className={`aspect-square rounded-md border border-line ${activityTone(day.count)}`} />
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">История изучения</p>
        <h2 className="mt-2 text-2xl text-ink">Последние сессии</h2>
        <div className="mt-4 space-y-4">
          {history.map((item) => (
            <div key={item.id} className="rounded-[22px] border border-line bg-paper/75 p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm text-ink">{item.title}</p>
                  <p className="mt-1 font-mono text-xs uppercase tracking-[0.22em] text-muted">{formatStatus(item.status)}</p>
                </div>
                <p className="text-xs text-muted">{new Date(item.lastOpenedAt).toLocaleDateString()}</p>
              </div>
              <div className="mt-3">
                <Meter value={item.progress} />
              </div>
            </div>
          ))}
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
