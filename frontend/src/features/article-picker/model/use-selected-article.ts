import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type SelectedArticleState = {
  selectedArticleId: string
  searchTerm: string
  setSelectedArticleId: (articleId: string) => void
  setSearchTerm: (value: string) => void
}

export const useSelectedArticle = create<SelectedArticleState>()(
  persist(
    (set) => ({
      selectedArticleId: '',
      searchTerm: 'llm agents',
      setSelectedArticleId: (selectedArticleId) => set({ selectedArticleId }),
      setSearchTerm: (searchTerm) => set({ searchTerm }),
    }),
    {
      name: 'science-helpy-page-state',
      partialize: (state) => ({
        selectedArticleId: state.selectedArticleId,
        searchTerm: state.searchTerm,
      }),
    },
  ),
)
