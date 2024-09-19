import { createRouter, createWebHistory } from 'vue-router'
import { loadLayoutMiddleware } from './middleware'
import HomeView from '../views/HomeView/HomeView.vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import NoneSidebarLayout from '@/layouts/NoneSidebarLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/space/bot' },
    {
      path: '/home',
      name: 'Home',
      component: HomeView,
      meta: { layout: DefaultLayout, requiresAuth: true }
    },
    {
      path: '/space',
      name: 'Personal',
      component: () => import('../views/PersonalView/PersonalView.vue'),
      meta: { layout: DefaultLayout, requiresAuth: true },
      children: [
        {
          path: 'bot',
          name: 'PersonalBot',
          component: () => import('@/views/PersonalView/PersonalBotView.vue')
        },
        {
          path: 'knowledge',
          name: 'PersonalKnowledge',
          component: () => import('@/views/PersonalView/PersonalKnowledgeView.vue')
        }
      ]
    },
    {
      path: '/space/bot/:botId',
      name: 'BotDetail',
      component: () => import('@/views/BotDetailView/BotDetailView.vue'),
      meta: { layout: NoneSidebarLayout, requiresAuth: true }
    },
    {
      path: '/space/knowledge/:knowledgeId',
      name: 'KnowledgeDetail',
      component: () => import('@/views/KnowledgeDetailView/KnowledgeDetailView.vue'),
      meta: { layout: DefaultLayout }
    },
    {
      path: '/space/knowledge/:knowledgeId/upload',
      name: 'UploadKnowledgeContent',
      component: () => import('@/views/UploadView/UploadView.vue'),
      meta: {layout: NoneSidebarLayout, requiresAuth: true}
    },
    {
      path: '/account',
      name: 'Account',
      component: () => import('../views/Account/AccountView.vue'),
      meta: { layout: DefaultLayout, requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login/LoginView.vue'),
      meta: { layout: NoneSidebarLayout }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFound/NotFound.vue'),
      meta: { layout: NoneSidebarLayout }
    }
  ]
})

router.beforeEach(loadLayoutMiddleware)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const tokenExpiration = localStorage.getItem('tokenExpiration')

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token || !tokenExpiration) {
      next({ name: 'Login' })
    } else if (new Date().getTime() > parseInt(tokenExpiration, 10)) {
      // Token hết hạn
      localStorage.removeItem('token')
      localStorage.removeItem('tokenExpiration')
      next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
