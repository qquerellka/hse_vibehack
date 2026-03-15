import { useQuery } from '@tanstack/react-query'
import { http } from '../../../shared/api/http'
import type { SessionHistoryItem } from '../../../shared/types/dashboard'

export function useHistory() {
  return useQuery({
    queryKey: ['history'],
    queryFn: async () => {
      const { data } = await http.get<{ items: SessionHistoryItem[] }>('/history')
      return data.items
    },
  })
}
