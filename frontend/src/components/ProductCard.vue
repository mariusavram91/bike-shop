<template>
  <div
    class="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow flex flex-col h-full"
  >
    <img
      :src="`/bike-${getRandomNumber()}.jpeg`"
      :alt="product.name"
      class="w-full max-h-85 object-cover rounded-md"
    />

    <div class="mt-4 flex-1 flex flex-col justify-end">
      <h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3>

      <p class="text-sm text-gray-600 mt-2">{{ product.description }}</p>

      <p class="text-xl font-bold text-gray-800 mt-4 text-center">{{ product.base_price }} €</p>

      <template v-if="!product.is_available || product.stock_quantity < 1">
        <span class="mt-4 w-full py-2 text-center text-red-500">Out of stock</span>
      </template>
      <template v-else>
        <button
          v-if="!product.is_custom"
          @click="addToCart"
          class="mt-4 w-full py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          Add to Cart
        </button>
        <button
          v-else
          @click="goToBuilder"
          class="mt-4 w-full py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors"
        >
          Customise
        </button></template
      >
    </div>
  </div>
</template>

<script lang="ts">
import type { Product } from '@/services/productsServices'

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object as () => Product,
      required: true,
    },
  },
  methods: {
    /**
     * Generates a random number between 1 and 6.
     * Used to dynamically determine the image for the product card.
     * @returns {number} A random integer between 1 and 6.
     */
    getRandomNumber(): number {
      return Math.floor(Math.random() * 6) + 1
    },

    /**
     * Emits an 'add-to-cart' event with the current product as the payload.
     * Triggered when the "Add to Cart" button is clicked.
     */
    addToCart() {
      this.$emit('add-to-cart', this.product)
    },

    /**
     * Emits a 'go-to-builder' event with the current product as the payload.
     * Triggered when the "Customise" button is clicked.
     * Used to navigate the user to a product customization interface.
     */
    goToBuilder() {
      this.$emit('go-to-builder', this.product)
    },
  },
}
</script>
