import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard View',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/RuangMeeting',
      name: 'Ruang Meeting',
      component: () => import('../views/RuangMeetingView.vue'),
    },
    {
          path: '/RuangMeeting/PesanRuangan',
          name: 'Pesan Ruangan',
          component: () => import('../views/PesanRuanganView.vue'),
        },
  ],
})

export default router
