// src/router.ts

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

import ProductsView from '@/views/ProductsView.vue'
import CustomProductBuilder from '@/views/CustomProductBuilder.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: ProductsView,
  },
  {
    path: '/builder/:productId',
    name: 'ProductBuilder',
    component: CustomProductBuilder,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    return { top: 0, behavior: 'smooth' }
  },
})

export default router
