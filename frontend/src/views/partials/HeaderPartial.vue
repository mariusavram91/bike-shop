<!-- src/views/partials/HeaderPartial.vue -->

<template>
  <header class="flex items-center justify-between text-white">
    <div>
      <router-link to="/" class="flex items-center">
        <img src="@/assets/logo.svg" alt="Logo" class="h-20 w-auto" />
      </router-link>
    </div>

    <nav class="flex space-x-4 font-bold">
      <router-link
        v-if="$route.path !== '/'"
        to="/"
        class="text-white hover:text-gray-300 transition-colors"
      >
        Home
      </router-link>
    </nav>
  </header>
</template>

<script lang="ts">
export default {
  name: 'HeaderPartial',
}
</script>
