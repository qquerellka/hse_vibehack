export type ArticleSummary = {
  id: string
  arxivId: string
  title: string
  authors: string[]
  published: string
  abstract: string
  tags: string[]
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
  pdfUrl?: string
  texUrl?: string
  localPdfPath?: string
  localTexPath?: string
  parsedContent?: string
}
