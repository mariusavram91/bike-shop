// src/components/__tests__/CustomProductBuilder.spec.ts

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import type { ProductPart } from '@/services/productsServices'

import BuilderWizard from '../BuilderWizard.vue'

const mockProductParts: ProductPart[] = [
  {
    id: '1',
    name: 'Frame',
    product_id: '1',
    variants: [
      {
        id: '1-1',
        part_id: '1',
        name: 'Aluminum Frame',
        price: 300,
      },
      {
        id: '1-2',
        part_id: '1',
        name: 'Carbon Fiber Frame',
        price: 500,
      },
    ],
  },
  {
    id: '2',
    name: 'Wheels',
    product_id: '1',
    variants: [
      {
        id: '2-1',
        part_id: '2',
        name: 'Standard Wheels',
        price: 150,
      },
      {
        id: '2-2',
        part_id: '2',
        name: 'Racing Wheels',
        price: 250,
      },
    ],
  },
]

describe('CustomProductBuilder.vue', () => {
  it('renders the base price and product title', () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    expect(wrapper.text()).toContain('Custom Product Builder')
    expect(wrapper.text()).toContain('Base Price: 500€')
  })

  it('renders product parts and their variants', () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const partHeaders = wrapper.findAll('h3')
    expect(partHeaders).toHaveLength(2)
    expect(partHeaders[0].text()).toBe('Frame')
    expect(partHeaders[1].text()).toBe('Wheels')

    const variantButtons = wrapper.findAll('button')
    expect(variantButtons).toHaveLength(4) // 2 variants per part
    expect(variantButtons[0].text()).toContain('Aluminum Frame (+300 €)')
    expect(variantButtons[1].text()).toContain('Carbon Fiber Frame (+500 €)')
  })

  it('updates selected choices and advances the step when a variant is selected', async () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const firstVariantButton = wrapper.find('button') // Select "Aluminum Frame"
    await firstVariantButton.trigger('click')

    expect(wrapper.vm.selectedChoices['1']).toEqual({
      name: 'Aluminum Frame',
      price: 300,
    })
    expect(wrapper.vm.currentStep).toBe(2)
  })

  it('displays the selected choice for a part', async () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const firstVariantButton = wrapper.find('button') // Select "Aluminum Frame"
    await firstVariantButton.trigger('click')

    const selectedChoiceText = wrapper.find('.text-sm').text()
    expect(selectedChoiceText).toContain('Aluminum Frame (+300 €)')
  })

  it('undoes the last action and reverts the current step', async () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const firstVariantButton = wrapper.find('button') // Select "Aluminum Frame"
    await firstVariantButton.trigger('click')
    await wrapper.vm.undo()

    expect(wrapper.vm.selectedChoices).toEqual({})
    expect(wrapper.vm.currentStep).toBe(1)
  })

  it('resets all selections and the step when reset is triggered', async () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const firstVariantButton = wrapper.find('button') // Select "Aluminum Frame"
    await firstVariantButton.trigger('click')
    await wrapper.vm.reset()

    expect(wrapper.vm.selectedChoices).toEqual({})
    expect(wrapper.vm.currentStep).toBe(1)
    expect(wrapper.vm.choicesHistory).toHaveLength(0)
  })

  it('disables the undo button when no history exists', () => {
    const wrapper = mount(BuilderWizard, {
      props: { productParts: mockProductParts },
    })

    const undoButton = wrapper.find('button:disabled')
    expect(undoButton.exists()).toBe(true)
    expect(undoButton.text()).toBe('Undo')
  })
})
