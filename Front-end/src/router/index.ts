import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ExchangeRate',
      name: 'ExchangeRate',
      component: () => import('../views/ExchangeRateView.vue')
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('../views/MapView.vue')
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: () => import('../views/RecommendView.vue')
    },
    {
      path: '/article',
      name: 'article',
      component: () => import('../views/ArticleView.vue')
    },
    {
      path: '/article/:id',
      name: 'articleDetail',
      component: () => import('../views/ArticleDetailView.vue')
    },
    {
      path: '/article/:id/put',
      name: 'article/Put',
      component: () => import('../views/PutArticleView.vue')
    },
    {
      path: '/article/post',
      name: 'article/post',
      component: () => import('../views/MakeArticleView.vue')
    }
  ]
})

export default router
