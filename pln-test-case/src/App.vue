<script setup>
import { RouterView } from 'vue-router'
import Navbar from '/src/components/layout/Navbar.vue'
import Sidebar from '/src/components/layout/Sidebar.vue'
</script>

<template>
  <Navbar/>
  <main class="flex flex-row">
    <Sidebar />
    <RouterView />
  </main>
</template>

<style scoped>
</style>
