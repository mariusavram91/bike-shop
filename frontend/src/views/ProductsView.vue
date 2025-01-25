<!-- src/views/ProductsView.vue -->

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    <ProductCard
      v-for="(product, index) in products"
      :key="index"
      :product="product"
      @add-to-cart="handleAddToCart"
      @go-to-builder="handleGoToBuilder"
    />
  </div>
</template>

<script lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import ProductCard from '@/components/ProductCard.vue'
import { useProductsStore } from '@/stores/useProductsStore'
import type { Product } from '@/services/productsServices'
import { useCartStore } from '@/stores/useCartStore'

export default {
  name: 'ProductsPage',
  components: {
    ProductCard,
  },
  setup() {
    const router = useRouter()
    const productsStore = useProductsStore()
    const cartStore = useCartStore()

    onMounted(async () => {
      await productsStore.getProducts()
      cartStore.loadCartFromLocalStorage()
    })

    const products = computed(() => productsStore.products)

    return {
      router,
      products,
      cartStore,
    }
  },
  methods: {
    /**
     * Handles the `add-to-cart` event emitted by the ProductCard component.
     * @param {Product} product - The product that was added to the cart.
     */
    handleAddToCart(product: Product) {
      this.cartStore.addToCart({
        product_id: product.id,
        total_price: product.base_price,
      })
    },

    /**
     * Handles the `go-to-builder` event emitted by the ProductCard component.
     *
     * Redirect to the custom product builder page.
     *
     * @param {Product} product - The product for which customisation is initiated.
     */
    handleGoToBuilder(product: Product) {
      this.router.push({ name: 'ProductBuilder', params: { productId: product.id } })
    },
  },
}
</script>
