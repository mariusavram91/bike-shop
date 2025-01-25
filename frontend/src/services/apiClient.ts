// src/services/apiClient.ts

import axios, { type AxiosInstance } from 'axios'


/**
 * ApiClient is a wrapper around Axios to simplify HTTP requests.
 * It provides methods for common HTTP actions (GET, POST, PUT, DELETE) 
 * with predefined configurations like base URL and headers.
 */
class ApiClient {
  private axiosInstance: AxiosInstance;

  /**
   * Creates an instance of ApiClient with a specified base URL.
   * @param {string} baseURL - The base URL for API requests.
   */
  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  async get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
    const response = await this.axiosInstance.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: unknown): Promise<T> {
    const response = await this.axiosInstance.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: unknown): Promise<T> {
    const response = await this.axiosInstance.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.axiosInstance.delete(url);
    return response.data;
  }
}

/**
 * Retrieves the base URL for the API from environment variables.
 * Defaults to 'http://localhost:8000/api/v1' if not specified.
 * @returns {string} The base URL for API requests.
 */
const getBaseURL = () => import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const apiClient = new ApiClient(getBaseURL())
export default apiClient