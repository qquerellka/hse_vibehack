import { delay, http, HttpResponse } from 'msw'
import { analytics, articleDetails, historyItems } from './data'
import type { ArticleSummary } from '../types/article'

function findArticle(articleId: string) {
  return articleDetails.find((article) => article.id === articleId)
}

function toArticleSummary(article: ArticleSummary) {
  return {
    id: article.id,
    title: article.title,
    authors: article.authors,
    published: article.published,
    abstract: article.abstract,
    tags: article.tags,
    readingMinutes: article.readingMinutes,
    difficulty: article.difficulty,
  }
}

export const handlers = [
  http.get('/api/articles', async ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('q')?.toLowerCase().trim() ?? ''

    const items = articleDetails.filter((article) => {
      if (!query) {
        return true
      }

      const haystack = [
        article.title,
        article.abstract,
        article.tags.join(' '),
        article.authors.join(' '),
      ]
        .join(' ')
        .toLowerCase()

      return haystack.includes(query)
    })

    await delay(350)

    return HttpResponse.json({
      items: items.map(toArticleSummary),
    })
  }),

  http.get('/api/articles/:articleId/evaluation', async ({ params }) => {
    const article = findArticle(params.articleId as string)

    if (!article) {
      return new HttpResponse(null, { status: 404 })
    }

    await delay(240)
    return HttpResponse.json(article.evaluation)
  }),

  http.get('/api/articles/:articleId/review', async ({ params }) => {
    const article = findArticle(params.articleId as string)

    if (!article) {
      return new HttpResponse(null, { status: 404 })
    }

    await delay(450)
    return HttpResponse.json({ sections: article.review })
  }),

  http.get('/api/articles/:articleId/quiz', async ({ params }) => {
    const article = findArticle(params.articleId as string)

    if (!article) {
      return new HttpResponse(null, { status: 404 })
    }

    await delay(220)
    return HttpResponse.json({ items: article.quiz })
  }),

  http.get('/api/articles/:articleId/recommendations', async ({ params }) => {
    const article = findArticle(params.articleId as string)

    if (!article) {
      return new HttpResponse(null, { status: 404 })
    }

    await delay(260)
    return HttpResponse.json({ items: article.recommendations.map(toArticleSummary) })
  }),

  http.get('/api/articles/:articleId', async ({ params }) => {
    const article = findArticle(params.articleId as string)

    if (!article) {
      return new HttpResponse(null, { status: 404 })
    }

    await delay(280)
    return HttpResponse.json({
      ...article,
      recommendations: article.recommendations.map(toArticleSummary),
    })
  }),

  http.get('/api/history', async () => {
    await delay(250)
    return HttpResponse.json({ items: historyItems })
  }),

  http.get('/api/analytics', async () => {
    await delay(220)
    return HttpResponse.json(analytics)
  }),
]
