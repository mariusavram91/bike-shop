<!-- src/App.vue -->

<template>
  <div class="flex flex-col min-h-screen pl-4 pr-4 pt-1 pb-1 bg-primary text-white">
    <HeaderPartial />

    <div class="flex flex-grow pt-4 pb-4">
      <router-view :key="$route.fullPath"></router-view>
    </div>

    <FooterPartial />
  </div>
</template>

<script lang="ts">
import FooterPartial from '@/views/partials/FooterPartial.vue'
import HeaderPartial from '@/views/partials/HeaderPartial.vue'

export default {
  components: {
    HeaderPartial,
    FooterPartial,
  },
}
</script>
