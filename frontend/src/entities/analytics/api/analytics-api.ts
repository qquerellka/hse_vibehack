import { useQuery } from '@tanstack/react-query'
import { http } from '../../../shared/api/http'
import type { LearningAnalytics } from '../../../shared/types/dashboard'

export function useAnalytics() {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const { data } = await http.get<LearningAnalytics>('/analytics')
      return data
    },
  })
}
