export interface ArticlesType{
  id: number,
  title: string,
  user: {
    id: number,
    username: string
  }
}