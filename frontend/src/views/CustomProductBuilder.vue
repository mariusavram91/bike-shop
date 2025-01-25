<!-- src/views/CustomProductBuilder.vue -->

<template>
  <div class="flex gap-20">
    <BuilderWizard
      :product="current_product || {}"
      :productParts="current_product?.parts || []"
      @total-price-calculated="handleTotalPrice"
    />

    <div
      class="w-full max-w-lg bg-white p-6 rounded-lg shadow-md text-black flex flex-col justify-between"
    >
      <img src="/bike-1.jpeg" class="w-full max-h-85 object-cover rounded-md" />

      <div class="flex justify-between">
        <span class="text-xl font-semibold">Total Price: </span>
        <span class="text-5xl font-bold"> {{ total_price }}€</span>
      </div>

      <button
        @click="addToCart"
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

    const total_price = ref<number>(0)

    onMounted(async () => {
      await productsStore.getProducts()
    })

    const current_product = productsStore.getProductById(props.productId)

    return { current_product, total_price }
  },
  methods: {
    addToCart() {
      console.log({ 'Adding custom product to the cart': this.current_product })
    },

    handleTotalPrice(total: number) {
      this.total_price = total
    },
  },
}
</script>
