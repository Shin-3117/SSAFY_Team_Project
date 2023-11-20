export interface ArticlesType{
  created_at: string,
  id: number,
  title: string,
  user: {
    id: number,
    username: string
  }
}