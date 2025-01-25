// src/components/__tests__/ProductCard.spec.ts

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import type { Product } from '@/services/productsServices'

import ProductCard from '../ProductCard.vue'

const mockProduct: Product = {
  id: '1',
  name: 'Test Bike',
  description: 'This is a test bike description.',
  category: 'Bikes',
  base_price: 499.99,
  is_custom: false,
  is_available: true,
  stock_quantity: 4,
  parts: [],
}

const customProduct: Product = {
  ...mockProduct,
  is_custom: true,
}

describe('ProductCard.vue', () => {
  it('renders product information correctly', () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct },
    })

    expect(wrapper.text()).toContain(mockProduct.name)
    expect(wrapper.text()).toContain(mockProduct.description)
    expect(wrapper.text()).toContain(`${mockProduct.base_price} €`)
  })

  it('displays the correct image source with a random number', () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct },
    })

    const img = wrapper.find('img')
    const srcRegex = /\/bike-\d\.jpeg/
    expect(img.attributes('src')).toMatch(srcRegex)
  })

  it('shows the "Add to Cart" button for non-custom products', () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct },
    })

    const addToCartButton = wrapper.find('button')
    expect(addToCartButton.exists()).toBe(true)
    expect(addToCartButton.text()).toBe('Add to Cart')
  })

  it('emits "add-to-cart" event when "Add to Cart" button is clicked', async () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct },
    })

    const addToCartButton = wrapper.find('button')
    await addToCartButton.trigger('click')

    expect(wrapper.emitted('add-to-cart')).toHaveLength(1)
    expect(wrapper.emitted('add-to-cart')![0]).toEqual([mockProduct])
  })

  it('shows the "Customise" button for custom products', () => {
    const wrapper = mount(ProductCard, {
      props: { product: customProduct },
    })

    const customiseButton = wrapper.find('button')
    expect(customiseButton.exists()).toBe(true)
    expect(customiseButton.text()).toBe('Customise')
  })

  it('emits "go-to-builder" event when "Customise" button is clicked', async () => {
    const wrapper = mount(ProductCard, {
      props: { product: customProduct },
    })

    const customiseButton = wrapper.find('button')
    await customiseButton.trigger('click')

    expect(wrapper.emitted('go-to-builder')).toHaveLength(1)
    expect(wrapper.emitted('go-to-builder')![0]).toEqual([customProduct])
  })
})
