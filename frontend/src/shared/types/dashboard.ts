export type SessionHistoryItem = {
  id: string
  articleId: string
  title: string
  lastOpenedAt: string
  progress: number
  status: 'queued' | 'reading' | 'reviewed' | 'mastered'
}

export type ActivityDay = {
  date: string
  count: number
}

export type LearningAnalytics = {
  totalRead: number
  totalReviewed: number
  quizAccuracy: number
  streak: number
  activity: ActivityDay[]
}
