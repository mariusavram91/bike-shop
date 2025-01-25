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
 */
export interface PartVariant {
    id: string
    part_id: string
    name: string
    price: number
}

/**
 * Fetches all available products from the API.
 * @returns {Promise<Product[]>} A promise resolving to an array of products.
 */
export const fetchProducts = async (): Promise<Product[]> => {
  return await apiClient.get<Product[]>('/products')
}