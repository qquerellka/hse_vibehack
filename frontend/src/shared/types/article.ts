export type ArticleSummary = {
  id: string
  title: string
  authors: string[]
  published: string
  abstract: string
  tags: string[]
  readingMinutes: number
  difficulty: 'Intro' | 'Intermediate' | 'Advanced'
}

export type Evaluation = {
  novelty: number
  rigor: number
  impact: number
  overall: number
  verdict: string
  pros: string[]
  cons: string[]
  reasoning: string
}

export type ReviewSection = {
  title: string
  body: string
}

export type QuizQuestion = {
  id: string
  question: string
  options: string[]
  answer: number
}

export type ArticleDetail = ArticleSummary & {
  journalFit: string
  whyItMatters: string
  keyIdeas: string[]
  status: 'fresh' | 'reviewed' | 'mastered'
  evaluation: Evaluation
  review: ReviewSection[]
  quiz: QuizQuestion[]
  recommendations: ArticleSummary[]
}
