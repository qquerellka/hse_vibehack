import { useState } from 'react'
import { BookOpen, BrainCircuit, ChevronRight, Sparkles, TestTube2 } from 'lucide-react'
import {
  useArticleDetail,
  useArticleEvaluation,
  useArticleQuiz,
  useArticleRecommendations,
  useArticleReview,
} from '../../entities/article/api/article-api'
import { useSelectedArticle } from '../../features/article-picker/model/use-selected-article'
import { Badge } from '../../shared/ui/badge'
import { Button } from '../../shared/ui/button'
import { Card } from '../../shared/ui/card'
import { Modal } from '../../shared/ui/dialog'
import { Meter } from '../../shared/ui/meter'

function formatDifficulty(value: string) {
  if (value === 'Advanced') return 'сложная'
  if (value === 'Intermediate') return 'средняя'
  if (value === 'Intro') return 'базовая'
  return value
}

export function ArticleHub() {
  const { selectedArticleId, setSelectedArticleId } = useSelectedArticle()
  const [quizOpen, setQuizOpen] = useState(false)
  const articleQuery = useArticleDetail(selectedArticleId)
  const evaluationQuery = useArticleEvaluation(selectedArticleId)
  const reviewQuery = useArticleReview(selectedArticleId)
  const quizQuery = useArticleQuiz(selectedArticleId)
  const recommendationsQuery = useArticleRecommendations(selectedArticleId)

  const article = articleQuery.data
  const evaluation = evaluationQuery.data
  const review = reviewQuery.data ?? []
  const quiz = quizQuery.data ?? []
  const recommendations = recommendationsQuery.data ?? []

  if (articleQuery.isLoading || evaluationQuery.isLoading) {
    return <Card className="min-h-[640px]">Загружаю карточку статьи...</Card>
  }

  if (articleQuery.isError || evaluationQuery.isError || !article || !evaluation) {
    return (
      <Card className="min-h-[640px] space-y-4">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Ошибка загрузки статьи</p>
        <h2 className="text-2xl text-ink">Не удалось загрузить данные статьи.</h2>
        <p className="max-w-xl text-sm text-muted">
          Обычно это значит, что один из mock endpoint не ответил или dev-сервер все еще отдает старую версию приложения.
        </p>
        <div className="rounded-[20px] border border-line bg-fog/80 p-4 font-mono text-xs text-muted">
          article: {articleQuery.status} | evaluation: {evaluationQuery.status}
        </div>
      </Card>
    )
  }

  return (
    <>
      <Card className="space-y-6">
        <div className="flex flex-wrap items-start justify-between gap-4 border-b border-line pb-6">
          <div className="max-w-2xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Текущая статья</p>
            <h1 className="mt-3 text-4xl leading-tight text-ink md:text-5xl">{article.title}</h1>
            <p className="mt-4 max-w-3xl text-base text-muted">{article.whyItMatters}</p>
          </div>
          <div className="space-y-2 rounded-[24px] border border-line bg-fog/80 p-4">
            <Badge>{formatDifficulty(article.difficulty)}</Badge>
            <p className="text-sm text-muted">{article.readingMinutes} мин чтения</p>
            <p className="text-sm text-muted">{article.authors.join(', ')}</p>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          {[
            { label: 'Новизна', value: evaluation.novelty * 20 },
            { label: 'Строгость', value: evaluation.rigor * 20 },
            { label: 'Влияние', value: evaluation.impact * 20 },
            { label: 'Итог', value: evaluation.overall * 20 },
          ].map((metric) => (
            <Card key={metric.label} className="rounded-[24px] bg-fog/70 p-4 shadow-none">
              <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">{metric.label}</p>
              <p className="mt-2 text-3xl text-ink">{metric.value / 20}/5</p>
              <div className="mt-3">
                <Meter value={metric.value} />
              </div>
            </Card>
          ))}
        </div>

        <div className="grid gap-5 xl:grid-cols-[1.25fr,0.75fr]">
          <div className="space-y-5">
            <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
              <div className="flex items-center gap-2">
                <BrainCircuit className="h-4 w-4 text-muted" />
                <h2 className="text-xl text-ink">Сводка оценки</h2>
              </div>
              <p className="mt-3 text-sm text-muted">{evaluation.verdict}</p>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">Плюсы</p>
                  <ul className="mt-3 space-y-2 text-sm text-ink">
                    {evaluation.pros.map((item) => (
                      <li key={item}>+ {item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">Минусы</p>
                  <ul className="mt-3 space-y-2 text-sm text-ink">
                    {evaluation.cons.map((item) => (
                      <li key={item}>- {item}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <p className="mt-4 text-sm leading-7 text-muted">{evaluation.reasoning}</p>
            </Card>

            <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
              <div className="flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-muted" />
                <h2 className="text-xl text-ink">Черновик обзора</h2>
              </div>
              <div className="prose-copy mt-4 space-y-4 text-sm leading-7 text-ink">
                {review.map((section) => (
                  <section key={section.title} className="border-t border-line pt-4 first:border-t-0 first:pt-0">
                    <h3 className="text-lg">{section.title}</h3>
                    <p className="mt-2 text-muted">{section.body}</p>
                  </section>
                ))}
              </div>
            </Card>
          </div>

          <div className="space-y-5">
            <Card className="rounded-[24px] bg-ink p-5 text-paper shadow-none">
              <p className="font-mono text-xs uppercase tracking-[0.22em] text-paper/60">Следующий шаг</p>
              <h2 className="mt-3 text-2xl text-paper">Закрепи материал коротким квизом.</h2>
              <p className="mt-3 text-sm text-paper/70">
                Это напрямую соответствует твоей идее: после каждой разобранной статьи можно давать мини-тест и подборку следующего чтения.
              </p>
              <Button variant="outline" className="mt-5 border-white/20 bg-white/10 text-paper" onClick={() => setQuizOpen(true)}>
                Открыть квиз
              </Button>
            </Card>

            <Card className="rounded-[24px] bg-fog/80 p-5 shadow-none">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-muted" />
                <h2 className="text-xl text-ink">Почему эта статья здесь</h2>
              </div>
              <p className="mt-3 text-sm leading-7 text-muted">{article.journalFit}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {article.keyIdeas.map((idea) => (
                  <Badge key={idea}>{idea}</Badge>
                ))}
              </div>
            </Card>

            <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
              <div className="flex items-center gap-2">
                <ChevronRight className="h-4 w-4 text-muted" />
                <h2 className="text-xl text-ink">Что читать дальше</h2>
              </div>
              <div className="mt-4 space-y-3">
                {recommendations.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setSelectedArticleId(item.id)}
                    className="w-full rounded-[20px] border border-line bg-paper/80 p-4 text-left transition-transform hover:-translate-y-0.5"
                  >
                    <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">{item.id}</p>
                    <h3 className="mt-2 text-base text-ink">{item.title}</h3>
                    <p className="mt-2 text-sm text-muted">{item.abstract}</p>
                  </button>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </Card>

      <Modal open={quizOpen} onOpenChange={setQuizOpen} title="Квиз на закрепление">
        <div className="space-y-5">
          {quiz.map((item, index) => (
            <Card key={item.id} className="rounded-[22px] bg-white/70 p-4 shadow-none">
              <div className="flex items-start gap-3">
                <div className="mt-1 rounded-full border border-line px-2 py-1 font-mono text-xs text-muted">
                  {index + 1}
                </div>
                <div className="space-y-3">
                  <p className="text-base text-ink">{item.question}</p>
                  <div className="grid gap-2">
                    {item.options.map((option, optionIndex) => (
                      <div
                        key={option}
                        className={`rounded-2xl border px-3 py-2 text-sm ${
                          optionIndex === item.answer ? 'border-ink bg-ink text-paper' : 'border-line bg-paper'
                        }`}
                      >
                        {option}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          ))}
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted">Позже сюда можно добавить отправку ответов и обновление аналитики.</p>
            <Button onClick={() => setQuizOpen(false)}>
              <TestTube2 className="mr-2 h-4 w-4" />
              Закрыть
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}
