// src/stores/useProductsStore.ts

import { defineStore } from 'pinia'
import { ref } from 'vue'

import { fetchProducts, type Product } from '@/services/productsServices'

export const useProductsStore = defineStore('productsStore', {
  state: () => ({
    products: ref<Product[]>([]),
  }),
  actions: {
    /**
     * Fetches the list of products from the API and updates the store's state.
     * Handles errors by logging them and resetting the `products` array to an empty state.
     */
    async getProducts() {
      try {
        const products = await fetchProducts()
        this.products = products
      } catch (error) {
        console.error('Failed to fetch products:', error)
        this.products = []
      }
    },

    /**
     * Retrieves a specific product by its ID.
     * @param {string} id - The ID of the product to retrieve.
     * @returns {Product | undefined} The matching product, or `undefined` if not found.
     */
    getProductById(id: string) {
        return this.products.find((product: Product) => product.id === id)
    },

    /**
     * Clears the products in the store, resetting the `products` array to an empty state.
     */
    clearProducts() {
      this.products = []
    },
  },
})
