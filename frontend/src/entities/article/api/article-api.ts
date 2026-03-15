import { useQuery } from '@tanstack/react-query'
import { http } from '../../../shared/api/http'
import type { ArticleDetail, ArticleSummary, Evaluation, QuizQuestion, ReviewSection } from '../../../shared/types/article'

export function useArticles(query: string) {
  return useQuery({
    queryKey: ['articles', query],
    queryFn: async () => {
      const { data } = await http.get<{ items: ArticleSummary[] }>('/articles', {
        params: { q: query },
      })
      return data.items
    },
  })
}

export function useArticleDetail(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId],
    queryFn: async () => {
      const { data } = await http.get<ArticleDetail>(`/articles/${articleId}`)
      return data
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleEvaluation(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'evaluation'],
    queryFn: async () => {
      const { data } = await http.get<Evaluation>(`/articles/${articleId}/evaluation`)
      return data
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleReview(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'review'],
    queryFn: async () => {
      const { data } = await http.get<{ sections: ReviewSection[] }>(`/articles/${articleId}/review`)
      return data.sections
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleQuiz(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'quiz'],
    queryFn: async () => {
      const { data } = await http.get<{ items: QuizQuestion[] }>(`/articles/${articleId}/quiz`)
      return data.items
    },
    enabled: Boolean(articleId),
  })
}

export function useArticleRecommendations(articleId: string) {
  return useQuery({
    queryKey: ['article', articleId, 'recommendations'],
    queryFn: async () => {
      const { data } = await http.get<{ items: ArticleSummary[] }>(`/articles/${articleId}/recommendations`)
      return data.items
    },
    enabled: Boolean(articleId),
  })
}
