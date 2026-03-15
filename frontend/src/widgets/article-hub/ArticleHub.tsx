import type { ReactNode } from 'react'
import { isAxiosError } from 'axios'
import {
  BookOpen,
  BrainCircuit,
  CalendarDays,
  ChevronRight,
  Download,
  ExternalLink,
  FileCode2,
  FileText,
  FolderSearch,
  LoaderCircle,
  ScrollText,
  Sparkles,
} from 'lucide-react'
import {
  useArticleDetail,
  useArticleEvaluation,
  useArticleParse,
  useArticleReview,
  useGenerateArticleEvaluation,
  useGenerateArticleReview,
} from '../../entities/article/api/article-api'
import { useSelectedArticle } from '../../features/article-picker/model/use-selected-article'
import type { Evaluation, Review } from '../../shared/types/article'
import { Badge } from '../../shared/ui/badge'
import { Button } from '../../shared/ui/button'
import { Card } from '../../shared/ui/card'
import { Meter } from '../../shared/ui/meter'
import { ProgressStatus } from '../../shared/ui/progress-status'

export function ArticleHub() {
  const { selectedArticleId, setSelectedArticleId } = useSelectedArticle()
  const articleQuery = useArticleDetail(selectedArticleId)
  const article = articleQuery.data
  const articleBackendId = article?.id ?? ''

  const parseMutation = useArticleParse(articleBackendId)
  const evaluationQuery = useArticleEvaluation(articleBackendId)
  const reviewQuery = useArticleReview(articleBackendId)
  const evaluationMutation = useGenerateArticleEvaluation(articleBackendId)
  const reviewMutation = useGenerateArticleReview(articleBackendId)

  const evaluation = evaluationQuery.data ?? null
  const review = reviewQuery.data ?? null

  const isDownloading = articleQuery.isLoading || articleQuery.isFetching
  const isParsing = parseMutation.isPending
  const isEvaluating = evaluationMutation.isPending
  const isWritingReview = reviewMutation.isPending
  const inferredParsing = !article?.parsedContent && (isEvaluating || isWritingReview)

  if (!selectedArticleId) {
    return (
      <Card className="min-h-[640px]">
        <div className="max-w-xl space-y-4">
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Workspace</p>
          <h2 className="text-3xl text-ink">Выберите статью из результатов поиска.</h2>
          <p className="text-sm leading-7 text-muted">
            После выбора frontend скачает карточку статьи через backend, покажет файлы, распарсенный текст, оценку и обзор.
          </p>
        </div>
      </Card>
    )
  }

  if (articleQuery.isLoading || (articleQuery.isFetching && !article)) {
    return (
      <Card className="min-h-[640px] space-y-4">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Pipeline</p>
        <h2 className="text-2xl text-ink">Скачиваю карточку статьи и файлы через backend.</h2>
        <LoadingBlock title="Идёт скачивание" description="Backend запрашивает метаданные статьи, PDF и TeX, затем создаёт внутреннюю запись с UUID." />
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <Step title="1. Download" description="скачивание статьи" state="active" />
          <Step title="2. Parse" description="ожидает завершения download" state="idle" />
          <Step title="3. Evaluate" description="ожидает завершения download" state="idle" />
          <Step title="4. Review" description="ожидает завершения download" state="idle" />
        </div>
      </Card>
    )
  }

  if (articleQuery.isError || !article) {
    return (
      <Card className="min-h-[640px] space-y-4">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Ошибка</p>
        <h2 className="text-2xl text-ink">Не удалось загрузить карточку статьи.</h2>
        <p className="max-w-xl text-sm leading-7 text-muted">
          Проверьте, что backend запущен, а orchestration layer может скачать статью по выбранному arXiv ID.
        </p>
        <div className="rounded-[20px] border border-line bg-fog/80 p-4 font-mono text-xs text-muted">
          {getErrorMessage(articleQuery.error)}
        </div>
      </Card>
    )
  }

  const pipelineSteps = [
    {
      title: '1. Download',
      description: isDownloading ? 'backend скачивает PDF и TeX' : article.localPdfPath || article.localTexPath ? 'файлы получены' : 'ожидает загрузки',
      state: isDownloading ? 'active' : article.localPdfPath || article.localTexPath ? 'done' : 'idle',
    },
    {
      title: '2. Parse',
      description: isParsing || inferredParsing ? 'извлекается текст статьи' : article.parsedContent ? 'parsed_content получен' : 'парсинг ещё не запускался',
      state: isParsing || inferredParsing ? 'active' : article.parsedContent ? 'done' : 'idle',
    },
    {
      title: '3. Evaluate',
      description: isEvaluating ? 'GraphMAS считает оценку' : evaluation ? 'оценка сохранена' : 'оценка ещё не запускалась',
      state: isEvaluating ? 'active' : evaluation ? 'done' : 'idle',
    },
    {
      title: '4. Review',
      description: isWritingReview ? 'генерируется обзор' : review ? 'обзор сохранён' : 'обзор ещё не запускался',
      state: isWritingReview ? 'active' : review ? 'done' : 'idle',
    },
  ] as const

  return (
    <Card className="space-y-6">
      <div className="space-y-5 border-b border-line pb-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-3xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-muted">Article dossier</p>
            <h1 className="mt-3 text-4xl leading-tight text-ink md:text-5xl">{article.title}</h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-muted">{article.abstract}</p>
          </div>
          <div className="min-w-[320px] space-y-3 rounded-[24px] border border-line bg-fog/80 p-5">
            <Badge>{article.arxivId}</Badge>
            <InfoRow label="UUID статьи" value={article.id} />
            <InfoRow label="Дата публикации" value={article.published} />
            <InfoRow label="Авторы" value={article.authors.join(', ')} />
            <div className="flex flex-wrap gap-2">
              {article.tags.length > 0 ? article.tags.map((tag) => <Badge key={tag}>{tag}</Badge>) : <Badge>Без категорий</Badge>}
            </div>
          </div>
        </div>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {pipelineSteps.map((step) => (
            <Step key={step.title} title={step.title} description={step.description} state={step.state} />
          ))}
        </div>

        <div className="flex flex-wrap gap-2">
          <Button type="button" variant="outline" onClick={() => articleQuery.refetch()} disabled={isDownloading}>
            {isDownloading ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : <Download className="mr-2 h-4 w-4" />}
            Обновить статью
          </Button>
          <Button type="button" variant="outline" onClick={() => parseMutation.mutate()} disabled={isParsing || !articleBackendId}>
            {isParsing ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : <FileText className="mr-2 h-4 w-4" />}
            Извлечь текст
          </Button>
          <Button type="button" variant="outline" onClick={() => reviewMutation.mutate()} disabled={isWritingReview || !articleBackendId}>
            {isWritingReview ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : <ScrollText className="mr-2 h-4 w-4" />}
            Краткая выжимка
          </Button>
          <Button type="button" onClick={() => evaluationMutation.mutate()} disabled={isEvaluating || !articleBackendId}>
            {isEvaluating ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : <BrainCircuit className="mr-2 h-4 w-4" />}
            Оценить статью
          </Button>
          <Button type="button" variant="outline" onClick={() => reviewMutation.mutate()} disabled={isWritingReview || !articleBackendId}>
            {isWritingReview ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
            Написать обзор
          </Button>
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.2fr,0.8fr]">
        <div className="space-y-5">
          <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
            <div className="flex items-center gap-2">
              <CalendarDays className="h-4 w-4 text-muted" />
              <h2 className="text-xl text-ink">Информация о статье</h2>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <ArtifactRow label="arXiv ID" value={article.arxivId} icon={<FolderSearch className="h-4 w-4" />} />
              <ArtifactRow label="Дата публикации" value={article.published} icon={<CalendarDays className="h-4 w-4" />} />
              <ArtifactRow label="Авторы" value={article.authors.join(', ')} icon={<FileCode2 className="h-4 w-4" />} />
              <ArtifactRow label="Категории" value={article.tags.length > 0 ? article.tags.join(', ') : 'Не указаны'} icon={<FolderSearch className="h-4 w-4" />} />
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {article.pdfUrl && (
                <a href={article.pdfUrl} target="_blank" rel="noreferrer" download>
                  <Button type="button" variant="outline">
                    <Download className="mr-2 h-4 w-4" />
                    Скачать PDF
                  </Button>
                </a>
              )}
              {article.texUrl && (
                <a href={article.texUrl} target="_blank" rel="noreferrer" download>
                  <Button type="button" variant="outline">
                    <Download className="mr-2 h-4 w-4" />
                    Скачать TeX
                  </Button>
                </a>
              )}
              {article.pdfUrl && (
                <a href={article.pdfUrl} target="_blank" rel="noreferrer">
                  <Button type="button" variant="ghost">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Открыть PDF
                  </Button>
                </a>
              )}
            </div>
          </Card>

          <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
            <div className="flex items-center gap-2">
              <ScrollText className="h-4 w-4 text-muted" />
              <h2 className="text-xl text-ink">Распарсенный текст</h2>
            </div>
            {parseMutation.isError && (
              <ErrorBlock message={getErrorMessage(parseMutation.error)} />
            )}
            {article.parsedContent ? (
              <TextBlock value={article.parsedContent} />
            ) : isParsing || inferredParsing ? (
              <LoadingBlock title="Извлекаю текст статьи" description="Backend парсит TeX или PDF и сохранит parsed_content в карточку статьи." />
            ) : (
              <p className="mt-4 text-sm leading-7 text-muted">parsed_content пока отсутствует. Запустите «Извлечь текст», оценку или обзор.</p>
            )}
          </Card>

          <SummaryPanel
            review={review}
            isGenerating={isWritingReview}
            errorMessage={reviewMutation.isError ? getErrorMessage(reviewMutation.error) : null}
          />

          <EvaluationPanel
            evaluation={evaluation}
            isLoading={evaluationQuery.isLoading}
            isGenerating={isEvaluating}
            errorMessage={evaluationQuery.isError ? getErrorMessage(evaluationQuery.error) : evaluationMutation.isError ? getErrorMessage(evaluationMutation.error) : null}
          />

          <ReviewPanel
            review={review}
            isLoading={reviewQuery.isLoading}
            isGenerating={isWritingReview}
            errorMessage={reviewQuery.isError ? getErrorMessage(reviewQuery.error) : reviewMutation.isError ? getErrorMessage(reviewMutation.error) : null}
          />
        </div>

        <div className="space-y-5">
          <Card className="rounded-[24px] bg-ink p-5 text-paper shadow-none">
            <p className="font-mono text-xs uppercase tracking-[0.22em] text-paper/60">Текущий pipeline</p>
            <h2 className="mt-3 text-2xl text-paper">Все ответы идут напрямую от backend.</h2>
            <div className="mt-4 space-y-3 text-sm text-paper/75">
              <p>Поиск возвращает arXiv результаты.</p>
              <p>Скачивание создаёт внутреннюю карточку статьи с UUID.</p>
              <p>Парсинг обновляет `parsed_content`.</p>
              <p>Оценка и обзор читаются из сохранённых backend-сущностей.</p>
            </div>
          </Card>

          <Card className="rounded-[24px] bg-fog/80 p-5 shadow-none">
            <div className="flex items-center gap-2">
              <FolderSearch className="h-4 w-4 text-muted" />
              <h2 className="text-xl text-ink">Технический статус</h2>
            </div>
            <div className="mt-4 space-y-3 text-sm text-muted">
              <InfoRow label="selectedArticleId" value={selectedArticleId} />
              <InfoRow label="download status" value={articleQuery.status} />
              <InfoRow label="evaluation query" value={evaluationQuery.status} />
              <InfoRow label="review query" value={reviewQuery.status} />
            </div>
          </Card>

          <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-muted" />
              <h2 className="text-xl text-ink">Действия с текущей статьёй</h2>
            </div>
            <div className="mt-4 space-y-3 text-sm text-muted">
              <p>Если backend уже сохранил оценку или обзор, frontend поднимет их автоматически через `GET` endpoint.</p>
              <p>Если данных ещё нет, можно отдельно запустить парсинг, оценку или написание обзора.</p>
              <Button type="button" variant="ghost" className="px-0 text-left text-ink" onClick={() => setSelectedArticleId(article.arxivId)}>
                Повторно открыть карточку по arXiv ID
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </Card>
  )
}

function EvaluationPanel({
  evaluation,
  isLoading,
  isGenerating,
  errorMessage,
}: {
  evaluation: Evaluation | null
  isLoading: boolean
  isGenerating: boolean
  errorMessage: string | null
}) {
  return (
    <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
      <div className="flex items-center gap-2">
        <BrainCircuit className="h-4 w-4 text-muted" />
        <h2 className="text-xl text-ink">Оценка статьи</h2>
      </div>

      {evaluation && (
        <>
          <div className="mt-4 grid gap-4 md:grid-cols-4">
            {[
              { label: 'Новизна', value: evaluation.novelty },
              { label: 'Строгость', value: evaluation.rigor },
              { label: 'Влияние', value: evaluation.impact },
              { label: 'Итог', value: evaluation.overall },
            ].map((metric) => (
              <Card key={metric.label} className="rounded-[24px] bg-fog/70 p-4 shadow-none">
                <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">{metric.label}</p>
                <p className="mt-2 text-3xl text-ink">{metric.value}/5</p>
                <div className="mt-3">
                  <Meter value={metric.value * 20} />
                </div>
              </Card>
            ))}
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <ArtifactRow label="evaluation.id" value={evaluation.id} icon={<FileCode2 className="h-4 w-4" />} />
            <ArtifactRow label="evaluation.article_id" value={evaluation.articleId} icon={<FileCode2 className="h-4 w-4" />} />
            <ArtifactRow label="category" value={evaluation.category} icon={<BrainCircuit className="h-4 w-4" />} />
            <ArtifactRow label="relevance" value={evaluation.relevance} icon={<Sparkles className="h-4 w-4" />} />
          </div>

          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <ListBlock title="Плюсы" items={evaluation.pros} prefix="+ " />
            <ListBlock title="Минусы" items={evaluation.cons} prefix="- " />
          </div>

          <div className="mt-4">
            <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">justification</p>
            <p className="mt-2 text-sm leading-7 text-muted">{evaluation.reasoning}</p>
          </div>
        </>
      )}

      {!evaluation && (isLoading || isGenerating) && (
        <LoadingBlock title="Получаю оценку статьи" description="Frontend ждёт, пока backend вернёт или сгенерирует `EvaluationResponse`." />
      )}

      {!evaluation && !isLoading && !isGenerating && !errorMessage && (
        <p className="mt-4 text-sm leading-7 text-muted">Оценка для статьи ещё не сохранена.</p>
      )}

      {errorMessage && <ErrorBlock message={errorMessage} />}
    </Card>
  )
}

function ReviewPanel({
  review,
  isLoading,
  isGenerating,
  errorMessage,
}: {
  review: Review | null
  isLoading: boolean
  isGenerating: boolean
  errorMessage: string | null
}) {
  return (
    <Card className="rounded-[24px] bg-white/65 p-5 shadow-none">
      <div className="flex items-center gap-2">
        <BookOpen className="h-4 w-4 text-muted" />
        <h2 className="text-xl text-ink">Обзор статьи</h2>
      </div>

      {review && (
        <>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <ArtifactRow label="review.id" value={review.id} icon={<FileCode2 className="h-4 w-4" />} />
            <ArtifactRow label="review.article_id" value={review.articleId} icon={<FileCode2 className="h-4 w-4" />} />
          </div>

          <div className="prose-copy mt-4 space-y-4 text-sm leading-7 text-ink">
            {review.sections.map((section) => (
              <section key={section.title} className="border-t border-line pt-4 first:border-t-0 first:pt-0">
                <h3 className="text-lg">{section.title}</h3>
                <p className="mt-2 whitespace-pre-wrap text-muted">{section.body || 'Пустой раздел'}</p>
              </section>
            ))}
          </div>

          <div className="mt-4">
            <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">full_text</p>
            <TextBlock value={review.fullText} />
          </div>
        </>
      )}

      {!review && (isLoading || isGenerating) && (
        <LoadingBlock title="Получаю обзор статьи" description="Frontend ждёт, пока backend вернёт или сгенерирует `ReviewResponse`." />
      )}

      {!review && !isLoading && !isGenerating && !errorMessage && (
        <p className="mt-4 text-sm leading-7 text-muted">Обзор для статьи ещё не сохранён.</p>
      )}

      {errorMessage && <ErrorBlock message={errorMessage} />}
    </Card>
  )
}

function SummaryPanel({
  review,
  isGenerating,
  errorMessage,
}: {
  review: Review | null
  isGenerating: boolean
  errorMessage: string | null
}) {
  return (
    <Card className="rounded-[24px] bg-fog/80 p-5 shadow-none">
      <div className="flex items-center gap-2">
        <ScrollText className="h-4 w-4 text-muted" />
        <h2 className="text-xl text-ink">Краткая выжимка</h2>
      </div>

      {review ? (
        <div className="mt-4 space-y-4">
          <div className="rounded-[20px] border border-line bg-white/70 p-4">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">summary</p>
            <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-ink">{review.summary}</p>
          </div>
          <div className="rounded-[20px] border border-line bg-white/70 p-4">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">verdict</p>
            <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-ink">{review.verdict}</p>
          </div>
        </div>
      ) : isGenerating ? (
        <LoadingBlock title="Генерирую краткую выжимку" description="Backend пишет обзор статьи, после чего здесь появится секция `summary` и итоговый `verdict`." />
      ) : (
        <div className="mt-4 rounded-[20px] border border-line bg-white/70 p-4 text-sm leading-7 text-muted">
          Краткая выжимка берётся из `summary` обзора. Нажмите кнопку `Краткая выжимка`, чтобы backend сгенерировал обзор и заполнил этот блок.
        </div>
      )}

      {errorMessage && <ErrorBlock message={errorMessage} />}

      {review && (
        <p className="mt-4 inline-flex items-center gap-2 text-sm text-muted">
          <ChevronRight className="h-4 w-4" />
          Полный обзор ниже раскрывает методы, результаты, критику и применение.
        </p>
      )}
    </Card>
  )
}

function Step({
  title,
  description,
  state,
}: {
  title: string
  description: string
  state: 'done' | 'active' | 'idle'
}) {
  const tone =
    state === 'done'
      ? 'border-ink bg-ink text-paper'
      : state === 'active'
        ? 'border-ink bg-white text-ink'
        : 'border-line bg-fog/70 text-muted'

  return (
    <div className={`rounded-[22px] border p-4 ${tone}`}>
      <p className="font-mono text-xs uppercase tracking-[0.22em]">{title}</p>
      <p className={`mt-2 text-sm leading-6 ${state === 'done' ? 'text-paper/80' : ''}`}>{description}</p>
      {(state === 'active' || state === 'done') && (
        <ProgressStatus
          active={state === 'active'}
          done={state === 'done'}
          estimateLabel="Обычно занимает около 2 минут."
        />
      )}
    </div>
  )
}

function ArtifactRow({ label, value, icon }: { label: string; value: string; icon: ReactNode }) {
  return (
    <div className="rounded-[18px] border border-line bg-fog/70 p-3">
      <div className="flex items-center gap-2 text-ink">
        {icon}
        <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{label}</p>
      </div>
      <p className="mt-2 break-all text-sm text-ink">{value}</p>
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{label}</p>
      <p className="mt-1 break-all text-sm text-ink">{value}</p>
    </div>
  )
}

function TextBlock({ value }: { value: string }) {
  return (
    <div className="mt-4 max-h-[420px] overflow-auto rounded-[20px] border border-line bg-fog/70 p-4">
      <pre className="whitespace-pre-wrap break-words font-sans text-sm leading-7 text-ink">{value}</pre>
    </div>
  )
}

function ListBlock({ title, items, prefix }: { title: string; items: string[]; prefix: string }) {
  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">{title}</p>
      {items.length > 0 ? (
        <ul className="mt-3 space-y-2 text-sm text-ink">
          {items.map((item) => (
            <li key={item}>
              {prefix}
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm text-muted">Пусто</p>
      )}
    </div>
  )
}

function LoadingBlock({ title, description }: { title: string; description: string }) {
  return (
    <div className="mt-4 rounded-[20px] border border-line bg-fog/70 p-4">
      <div className="flex items-center gap-2 text-ink">
        <LoaderCircle className="h-4 w-4 animate-spin" />
        <p className="text-sm">{title}</p>
      </div>
      <p className="mt-2 text-sm leading-7 text-muted">{description}</p>
      <ProgressStatus active estimateLabel="Обычно занимает около 2 минут." />
    </div>
  )
}

function ErrorBlock({ message }: { message: string }) {
  return (
    <div className="mt-4 rounded-[20px] border border-red-200 bg-red-50 p-4 text-sm text-red-700">
      {message}
    </div>
  )
}

function getErrorMessage(error: unknown) {
  if (isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    return error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Неизвестная ошибка.'
}
