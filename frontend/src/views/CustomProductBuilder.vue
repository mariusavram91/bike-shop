<!-- src/views/CustomProductBuilder.vue -->

<template>
  <div class="w-full flex gap-20">
    <BuilderWizard
      :product="current_product"
      :productParts="current_product?.parts || []"
      @total-price-calculated="handleTotalPrice"
      @selected-parts="handleSelectedVariants"
      class="w-1/2"
    />

    <div
      class="w-1/2 max-w-lg bg-white p-6 rounded-lg shadow-md text-black flex flex-col justify-between"
    >
      <img src="/bike-1.jpeg" class="w-full max-h-85 object-cover rounded-md" />

      <div class="flex justify-between">
        <span class="text-xl font-semibold">Total Price: </span>
        <span class="text-5xl font-bold"> {{ total_price }}€</span>
      </div>

      <button
        @click="addToCart"
        :disabled="!total_price"
        class="mt-4 w-full py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors"
      >
        Add to Cart
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted, ref } from 'vue'

import BuilderWizard from '@/components/BuilderWizard.vue'
import { useProductsStore } from '@/stores/useProductsStore'
import { useCartStore } from '@/stores/useCartStore'
import { type PartVariant, type Product } from '@/services/productsServices'

export default {
  components: {
    BuilderWizard,
  },
  props: {
    productId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const productsStore = useProductsStore()
    const cartStore = useCartStore()

    const current_product = ref<Partial<Product>>({
      id: '',
      name: '',
      parts: [],
    })

    const total_price = ref<number>(0)
    const selected_parts = ref<string>('')

    onMounted(async () => {
      await productsStore.getProducts()
      cartStore.loadCartFromLocalStorage()

      const product = productsStore.getProductById(props.productId)
      if (product) {
        current_product.value = product
      }
    })

    return { current_product, total_price, cartStore, selected_parts }
  },
  methods: {
    addToCart() {
      this.cartStore.addToCart({
        product_id: this.current_product?.id,
        total_price: this.total_price,
        selected_parts: this.selected_parts,
      })
    },

    handleTotalPrice(total: number) {
      this.total_price = total
    },

    handleSelectedVariants(variants: PartVariant[]) {
      this.selected_parts = Object.keys(variants).join(',')
    },
  },
}
</script>
