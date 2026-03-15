import { create } from 'zustand'

type SelectedArticleState = {
  selectedArticleId: string
  searchTerm: string
  setSelectedArticleId: (articleId: string) => void
  setSearchTerm: (value: string) => void
}

export const useSelectedArticle = create<SelectedArticleState>((set) => ({
  selectedArticleId: '2601.11464',
  searchTerm: '',
  setSelectedArticleId: (selectedArticleId) => set({ selectedArticleId }),
  setSearchTerm: (searchTerm) => set({ searchTerm }),
}))
