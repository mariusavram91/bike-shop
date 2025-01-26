// src/services/productsServices.ts

import apiClient from '@/services/apiClient'

/**
 * Interface representing a product.
 * Products are the main items sold in the application (i.e., bicycles).
 */
export interface Product {
  id: string
  name: string
  description: string
  category: string
  base_price: number
  is_custom: boolean
  is_available: boolean
  stock_quantity: number

  parts: ProductPart[]
}

/**
 * Interface representing a part of a product.
 * Parts are customisable components of a product (e.g., Frame, Wheels).
 */
export interface ProductPart {
  id: string
  name: string
  product_id: string

  variants: PartVariant[]
}

/**
 * Interface representing a variant of a product part.
 * Variants are specific options for a part (e.g., Full-suspension for Frame).
 * Variants can have restrictions based on other variants and are incompatible.
 * Variants can also have dynamic pricing based on other variants.
 */
export interface PartVariant {
  id: string
  part_id: string
  name: string
  price: number
  is_available: boolean
  stock_quantity: number

  custom_prices: CustomPrice[]
  dependencies: VariantDependency[]
}

/**
 * Interface representing a custom price for a part variant.
 * The variant_id is the one that the custom price applies to depending on if
 * dependent_variant_id is selected or not.
 * The custom_price is an addition on top of the PartVariant.price, it doesn't
 * replace the price.
 */
export interface CustomPrice {
    variant_id: string
    dependent_variant_id: string
    custom_price: number
}

/**
 * Interface representing a list of restricting variant ids for variant_id.
 * restrictions contains a comma separated list of uuid of other variants.
 * All these ids are incompatible with variant_id and vice versa.
 */
export interface VariantDependency {
    variant_id: string
    restrictions: string
}

/**
 * Fetches all available products from the API.
 * @returns {Promise<Product[]>} A promise resolving to an array of products.
 */
export const fetchProducts = async (): Promise<Product[]> => {
  return await apiClient.get<Product[]>('/products')
}
