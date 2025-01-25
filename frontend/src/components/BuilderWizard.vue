<template>
  <div class="w-full max-w-lg bg-white p-6 rounded-lg shadow-md flex flex-col">
    <h2 class="text-2xl text-black font-semibold mb-6 text-left">Custom Product Builder</h2>
    <div class="text-m text-black mb-6">Base Price: {{ product.base_price }}€</div>

    <div v-for="(part, index) in productParts" :key="part.id">
      <div class="mb-6">
        <h3 class="text-xl text-black font-semibold mb-4">{{ part.name }}</h3>

        <div v-if="currentStep === index + 1">
          <button
            v-for="variant in part.variants"
            :key="variant.id"
            :class="[
              'block w-full py-2 mb-2 rounded transition-colors',
              variant.is_available
                ? 'bg-blue-500 text-white hover:bg-blue-600'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed',
            ]"
            :disabled="!variant.is_available"
            @click="selectChoice(index + 1, part.id, variant.name, variant.price)"
          >
            {{ variant.name }} (+{{ variant.price }} €)
            <span class="text-sm text-red-500" v-if="!variant.is_available">Not in stock</span>
          </button>
        </div>

        <div v-else-if="selectedChoices[part.id]" class="mt-4">
          <p class="text-sm text-gray-700">
            <strong>{{ selectedChoices[part.id].name }}</strong> (+{{
              selectedChoices[part.id].price
            }}
            €)
          </p>
        </div>
      </div>
    </div>

    <div class="mt-auto flex space-x-4 justify-end">
      <button
        class="flex justify-center items-center gap-2 py-2 px-4 bg-gray-300 text-gray-700 rounded"
        :class="[
          choicesHistory.length === 0
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-gray-300 text-gray-700 hover:bg-gray-400',
        ]"
        @click="undo"
        :disabled="choicesHistory.length === 0"
      >
        Undo
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-arrow-counterclockwise"
          viewBox="0 0 16 16"
        >
          <path
            fill-rule="evenodd"
            d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"
          />
          <path
            d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"
          />
        </svg>
      </button>
      <button
        class="flex justify-center items-center gap-2 py-2 px-4 bg-red-500 text-white rounded hover:bg-red-600"
        @click="reset"
      >
        Reset
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-arrow-repeat"
          viewBox="0 0 16 16"
        >
          <path
            d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9"
          />
          <path
            fill-rule="evenodd"
            d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import type { Product, ProductPart } from '@/services/productsServices'

export default {
  props: {
    product: {
      type: Object as () => Product,
      required: true,
    },
    productParts: {
      type: Array as () => ProductPart[],
      required: true,
    },
  },
  data() {
    return {
      currentStep: 1,
      selectedChoices: {} as Record<string, { name: string; price: number }>,
      choicesHistory: [] as Array<Record<string, { name: string; price: number }>>,
      totalPrice: null as number | null,
    }
  },
  mounted() {
    this.calculateTotalPrice()
  },
  methods: {
    /**
     * Selects a variant for a given product part and progresses to the next step.
     * @param {number} step - Current step in the customisation process.
     * @param {string} partId - ID of the product part.
     * @param {string} choiceName - Name of the selected variant.
     * @param {number} choicePrice - Price of the selected variant.
     */
    selectChoice(step: number, partId: string, choiceName: string, choicePrice: number) {
      this.choicesHistory.push({ ...this.selectedChoices })

      this.selectedChoices[partId] = { name: choiceName, price: choicePrice }

      this.calculateTotalPrice()

      if (step < this.productParts.length + 1) {
        this.currentStep++
      }

      this.$emit('selected-parts', this.selectedChoices)
    },

    /**
     * Undoes the last selection by restoring the previous state.
     */
    undo() {
      if (this.choicesHistory.length > 0) {
        const previousState = this.choicesHistory.pop()
        if (previousState) {
          this.selectedChoices = { ...previousState }
          this.calculateTotalPrice()
          this.currentStep--
        }
      }

      this.$emit('selected-parts', this.selectedChoices)
    },

    /**
     * Resets the customisation process, clearing all selections.
     */
    reset() {
      this.selectedChoices = {}
      this.currentStep = 1
      this.choicesHistory = []
      this.calculateTotalPrice()
      this.$emit('selected-parts', this.selectedChoices)
    },

    /**
     * Calculates the total price based on the base price and selected choices.
     * Emits the total price to the parent component (used to show the updated price
     * in the preview card).
     */
    calculateTotalPrice() {
      const additionalPrice = Object.values(this.selectedChoices).reduce(
        (sum, choice) => sum + choice.price,
        0,
      )
      this.totalPrice = this.product.base_price + additionalPrice

      this.$emit('total-price-calculated', this.totalPrice)
    },
  },
}
</script>

<style scoped>
button {
  transition: all 0.3s ease;
}
</style>
