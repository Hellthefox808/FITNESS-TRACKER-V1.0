/**
 * Enterprise Authentication Service
 * Manages login, registration, token storage, and logout.
 * Author: Ravi Ranjan Singh
 */

import { apiClient } from './apiClient';

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  age?: number;
  gender?: string;
  height_cm?: number;
  weight_kg?: number;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  status: string;
  access_token?: string;
  refresh_token?: string;
  token_type?: string;
  expires_in?: number;
  message?: string;
  data?: any;
}

export class AuthService {
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>('/auth/register', payload, { skipAuth: true });
  }

  async login(payload: LoginPayload): Promise<AuthResponse> {
    const res = await apiClient.post<AuthResponse>('/auth/login', payload, { skipAuth: true });
    if (res.access_token) {
      localStorage.setItem('fitai_access_token', res.access_token);
      if (res.refresh_token) {
        localStorage.setItem('fitai_refresh_token', res.refresh_token);
      }
    }
    return res;
  }

  logout(): void {
    localStorage.removeItem('fitai_access_token');
    localStorage.removeItem('fitai_refresh_token');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('fitai_access_token');
  }
}

export const authService = new AuthService();
