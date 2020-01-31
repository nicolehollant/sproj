import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/model',
      name: 'model',
      component: () => import('./views/Model.vue')
    },
    {
      path: '/thesaurus',
      name: 'thesaurus',
      component: () => import('./views/Thesaurus.vue')
    },
    {
      path: '/writing',
      name: 'writing',
      component: () => import('./views/Writing.vue')
    },
    {
      path: '/midway',
      name: 'Midway',
      component: () => import('./views/Midway.vue')
    },
    {
      path: '/docs',
      name: 'docs',
      component: () => import('./views/Documentation.vue')
    }
  ]
})
