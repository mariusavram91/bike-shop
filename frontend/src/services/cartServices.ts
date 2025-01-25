// src/services/cartServices.ts

import apiClient from '@/services/apiClient'

export interface Cart {
    id: string
    purchased: boolean
    total_price: number
  
    items: Partial<CartItem>[]
}

export interface CartItem {
    id: string
    cart_id: string
    product_id: string
    selected_parts: string
    total_price: number
}

export const saveCart = async (cart: Partial<Cart>): Promise<Cart> => {
  return await apiClient.post<Cart>('/carts', cart)
}