import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'


Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/admin',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/dashboard',
      component: () => import('../views/UserDashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/packages',
      component: () => import('../views/Packages.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/invoices',
      component: () => import('../views/Invoices.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '*',
      redirect: '/dashboard'
    }
  ]
})

// Simple auth guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.isLoggedIn
  const isAdmin = store.getters.isAdmin
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/dashboard')
  } else if (to.path === '/login' && isLoggedIn) {
    next(isAdmin ? '/admin' : '/dashboard')
  } else {
    next()
  }
})

export default router