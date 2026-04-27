import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import { Layout } from '@/utils/routerHelper'
import { NO_RESET_WHITE_LIST } from '@/constants'

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard/analysis',
    name: 'Root',
    meta: { hidden: true }
  },
  {
    path: '/redirect',
    component: Layout,
    name: 'RedirectWrap',
    children: [
      {
        path: '/redirect/:path(.*)',
        name: 'Redirect',
        component: () => import('@/views/Redirect/Redirect.vue'),
        meta: {}
      }
    ],
    meta: { hidden: true, noTagsView: true }
  },
  {
    path: '/login',
    component: () => import('@/views/Login/Login.vue'),
    name: 'Login',
    meta: { hidden: true, title: 'Login', noTagsView: true }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: { hidden: true, title: '404', noTagsView: true }
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/analysis',
    name: 'Dashboard',
    meta: {
      title: 'Dashboard',
      icon: 'vi-ant-design:dashboard-filled',
      alwaysShow: true
    },
    children: [
      {
        path: 'analysis',
        component: () => import('@/views/Dashboard/Analysis.vue'),
        name: 'Analysis',
        meta: { title: 'Resumen de Red', noCache: true, affix: true }
      }
    ]
  },
  {
    path: '/network',
    component: Layout,
    redirect: '/network/switches',
    name: 'Network',
    meta: {
      title: 'Administración de Red',
      icon: 'vi-ant-design:cloud-server-outlined',
      alwaysShow: true
    },
    children: [
      {
        path: 'switches',
        component: () => import('@/views/Switches/List.vue'),
        name: 'Switches',
        meta: { title: 'Switches', noCache: true }
      },
      {
        path: 'topology',
        component: () => import('@/views/Topology/NetworkMap.vue'),
        name: 'Topology',
        meta: { title: 'Mapa Topológico', noCache: true }
      },
      {
        path: 'ssh-console/:id',
        component: () => import('@/views/SshConsole/Terminal.vue'),
        name: 'SshConsole',
        meta: { title: 'Consola SSH', hidden: true, noCache: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  const resetWhiteNameList = NO_RESET_WHITE_LIST
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !resetWhiteNameList.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
