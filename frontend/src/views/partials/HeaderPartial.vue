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
      <router-link
        v-if="$route.path !== '/cart'"
        to="/cart"
        class="flex text-white hover:text-gray-300 transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path
            d="M0 2.5A.5.5 0 0 1 .5 2H2a.5.5 0 0 1 .485.379L2.89 4H14.5a.5.5 0 0 1 .485.621l-1.5 6A.5.5 0 0 1 13 11H4a.5.5 0 0 1-.485-.379L1.61 3H.5a.5.5 0 0 1-.5-.5M3.14 5l.5 2H5V5zM6 5v2h2V5zm3 0v2h2V5zm3 0v2h1.36l.5-2zm1.11 3H12v2h.61zM11 8H9v2h2zM8 8H6v2h2zM5 8H3.89l.5 2H5zm0 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2m-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0m9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0"
          />
        </svg>

        <span
          v-if="cartStore.cart && cartStore.cart.items && cartStore.cart.items.length > 0"
          class="bg-red-500 text-white w-3 h-3 p-1.5 rounded-full flex justify-center items-center text-[10px] font-bold"
          >{{ cartStore.cart.items.length }}
        </span>
      </router-link>
    </nav>
  </header>
</template>

<script lang="ts">
import { onMounted } from 'vue'

import { useCartStore } from '@/stores/useCartStore'

export default {
  name: 'HeaderPartial',
  setup() {
    const cartStore = useCartStore()

    onMounted(() => {
      cartStore.loadCartFromLocalStorage()
    })

    return {
      cartStore,
    }
  },
}
</script>
