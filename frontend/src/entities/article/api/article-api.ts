import { useQuery } from '@tanstack/react-query'
import { http } from '../../../shared/api/http'
import type { ArticleDetail, ArticleSummary, Evaluation, QuizQuestion, ReviewSection } from '../../../shared/types/article'

type BackendArticle = {
  id: string
  arxiv_id: string
  title: string
  authors: string[]
  abstract: string
  published_date: string | null
  categories: string[]
  pdf_url?: string | null
  tex_url?: string | null
  local_pdf_path?: string | null
  local_tex_path?: string | null
  parsed_content?: string | null
}

type BackendEvaluation = {
  novelty_score: number
  methodology_score: number
  impact_score: number
  overall_score: number
  pros: string[]
  cons: string[]
  justification: string
  relevance: string
}

type BackendReview = {
  summary: string
  methods: string
  results: string
  criticism: string
  application: string
  verdict: string
}

function mapArticle(article: BackendArticle): ArticleDetail {
  return {
    id: article.id,
    arxivId: article.arxiv_id,
    title: article.title,
    authors: article.authors,
    published: article.published_date ? new Date(article.published_date).toLocaleDateString('ru-RU') : 'Дата не указана',
    abstract: article.abstract,
    tags: article.categories,
    pdfUrl: article.pdf_url ?? undefined,
    texUrl: article.tex_url ?? undefined,
    localPdfPath: article.local_pdf_path ?? undefined,
    localTexPath: article.local_tex_path ?? undefined,
    parsedContent: article.parsed_content ?? undefined,
  }
}

function mapEvaluation(evaluation: BackendEvaluation): Evaluation {
  return {
    novelty: evaluation.novelty_score,
    rigor: evaluation.methodology_score,
    impact: evaluation.impact_score,
    overall: evaluation.overall_score,
    verdict: evaluation.relevance,
    pros: evaluation.pros,
    cons: evaluation.cons,
    reasoning: evaluation.justification,
  }
}

function mapReview(review: BackendReview): ReviewSection[] {
  return [
    { title: 'Резюме', body: review.summary },
    { title: 'Методы', body: review.methods },
    { title: 'Результаты', body: review.results },
    { title: 'Критика', body: review.criticism },
    { title: 'Применение', body: review.application },
    { title: 'Вердикт', body: review.verdict },
  ]
}

export function useArticles(query: string) {
  return useQuery({
    queryKey: ['articles', query],
    queryFn: async () => {
      if (!query.trim()) {
        return []
      }

      const { data } = await http.post<BackendArticle[]>('/articles/search', {
        query,
        max_results: 10,
      })

      return data.map((article) => ({
        id: article.arxiv_id,
        arxivId: article.arxiv_id,
        title: article.title,
        authors: article.authors,
        published: article.published_date ? new Date(article.published_date).toLocaleDateString('ru-RU') : 'Дата не указана',
        abstract: article.abstract,
        tags: article.categories,
      }))
    },
    enabled: Boolean(query.trim()),
  })
}

export function useArticleDetail(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId],
    queryFn: async () => {
      const { data } = await http.post<BackendArticle>('/articles/download', {
        arxiv_id: articleId,
      })
      return mapArticle(data)
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleEvaluation(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'evaluation'],
    queryFn: async () => {
      const { data } = await http.post<BackendEvaluation>('/evaluations/evaluate', {
        article_id: articleId,
      })
      return mapEvaluation(data)
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleReview(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'review'],
    queryFn: async () => {
      const { data } = await http.post<BackendReview>('/reviews/write', {
        article_id: articleId,
      })
      return mapReview(data)
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleQuiz(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'quiz'],
    queryFn: async () => {
      return [] as QuizQuestion[]
    },
    enabled: false,
  })
}

export function useArticleRecommendations(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'recommendations'],
    queryFn: async () => {
      return [] as ArticleSummary[]
    },
    enabled: false,
  })
}
