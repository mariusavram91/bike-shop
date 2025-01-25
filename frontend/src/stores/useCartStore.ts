// src/stores/useCartStore.ts

import { ref } from 'vue'
import { defineStore } from 'pinia'

import { saveCart, type Cart, type CartItem } from '@/services/cartServices'

export const useCartStore = defineStore('cartStore', {
  state: () => ({
    cart: ref<Partial<Cart> | null>(null),
  }),
  actions: {
    /**
     * Adds an item to the cart. If the cart doesn't exist, it initialises a new cart.
     * Recalculates the total price of the cart and updates local storage.
     *
     * @param item - The item to add to the cart, which is a partial CartItem.
     */
    async addToCart(item: Partial<CartItem>) {
      if (!this.cart) {
        this.cart = {
          purchased: false,
          total_price: 0,
          items: [],
        }
      }

      this.cart.items?.push(item) // This will add duplicates at the moment

      if (this.cart.items) {
        this.cart.total_price = this.cart.items.reduce((total: number, item: Partial<CartItem>) => {
          if (item.total_price !== undefined) {
            return total + item.total_price
          }
          return total
        }, 0)
      }

      this.saveCartToLocalStorage()

      // This will keep adding new carts to the databse, it should actually
      // update the existing cart instead. Could save the id of the cart the
      // first time, then use it to update the cart.
      await this.saveCartToApi()
    },

    /**
     * Saves the current cart to localStorage.
     * This stores the cart data as a JSON string to persist the data across sessions.
     */
    saveCartToLocalStorage() {
      if (this.cart) {
        localStorage.setItem('cart', JSON.stringify(this.cart))
      }
    },

    /**
     * Asynchronously saves the cart data to an API (backend).
     * It handles potential errors when attempting to save the cart to the server.
     */
    async saveCartToApi() {
      try {
        if (this.cart) {
          await saveCart(this.cart)
          console.log('Cart successfully saved to API.')
        }
      } catch (error) {
        console.error('Failed to save cart to API:', error)
      }
    },

    /**
     * Loads the cart from localStorage if it exists.
     * If no cart data is found, it initialises a new cart.
     */
    loadCartFromLocalStorage() {
      const storedCart = localStorage.getItem('cart')
      if (storedCart) {
        this.cart = JSON.parse(storedCart)
      } else {
        this.cart = {
          purchased: false,
          total_price: 0,
          items: [],
        }
      }
    },

    /**
     * Clears the cart and removes it from localStorage.
     * This action resets the cart to its initial state.
     */
    clearCart() {
      this.cart = {
        purchased: false,
        total_price: 0,
        items: [],
      }
      localStorage.removeItem('cart')
    },
  },
})
