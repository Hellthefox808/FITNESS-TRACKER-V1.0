/**
 * Enterprise Centralized API Client
 * Features: Request Deduplication, Cancellation (AbortController),
 * Exponential Backoff Retries, Typed Responses, and Normalized Error Handling.
 * Author: Ravi Ranjan Singh
 */

export interface ApiErrorResponse {
  status: 'error';
  status_code: number;
  error_code: string;
  message: string;
  timestamp: string;
}

export interface RequestOptions extends RequestInit {
  timeoutMs?: number;
  retries?: number;
  backoffMs?: number;
  skipAuth?: boolean;
}

class EnterpriseApiClient {
  private baseUrl: string;
  private defaultTimeout: number;
  private pendingRequests: Map<string, Promise<any>>;

  constructor(baseUrl: string = 'http://localhost:8000/api/v1', defaultTimeout: number = 5000) {
    this.baseUrl = baseUrl;
    this.defaultTimeout = defaultTimeout;
    this.pendingRequests = new Map();
  }

  private getAuthToken(): string | null {
    return localStorage.getItem('fitai_access_token');
  }

  private normalizeError(error: any, statusCode: number = 500): ApiErrorResponse {
    if (error && error.status === 'error' && error.message) {
      return {
        status: 'error',
        status_code: statusCode,
        error_code: error.error_code || 'API_ERROR',
        message: error.message,
        timestamp: new Date().toISOString(),
      };
    }

    return {
      status: 'error',
      status_code: statusCode,
      error_code: statusCode === 401 ? 'UNAUTHORIZED' : statusCode === 403 ? 'FORBIDDEN' : 'NETWORK_ERROR',
      message: error?.message || 'An unexpected network error occurred. Please try again.',
      timestamp: new Date().toISOString(),
    };
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const {
      timeoutMs = this.defaultTimeout,
      retries = 2,
      backoffMs = 500,
      skipAuth = false,
      headers = {},
      ...fetchOptions
    } = options;

    const url = `${this.baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
    const requestKey = `${fetchOptions.method || 'GET'}:${url}:${JSON.stringify(fetchOptions.body || {})}`;

    // Request Deduplication for GET requests
    if ((fetchOptions.method || 'GET') === 'GET' && this.pendingRequests.has(requestKey)) {
      return this.pendingRequests.get(requestKey) as Promise<T>;
    }

    const requestPromise = (async () => {
      let lastError: any = null;

      for (let attempt = 0; attempt <= retries; attempt++) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
          const requestHeaders: Record<string, string> = {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            ...(headers as Record<string, string>),
          };

          if (!skipAuth) {
            const token = this.getAuthToken();
            if (token) {
              requestHeaders['Authorization'] = `Bearer ${token}`;
            }
          }

          const response = await fetch(url, {
            ...fetchOptions,
            headers: requestHeaders,
            signal: controller.signal,
          });

          clearTimeout(timeoutId);

          if (!response.ok) {
            let errorJson: any = {};
            try {
              errorJson = await response.json();
            } catch {
              /* ignore parse error */
            }
            const normalized = this.normalizeError(errorJson, response.status);
            
            // Retry only on server 5xx errors or network timeout
            if (response.status >= 500 && attempt < retries) {
              lastError = normalized;
              await new Promise((r) => setTimeout(r, backoffMs * Math.pow(2, attempt)));
              continue;
            }

            throw normalized;
          }

          const data = await response.json();
          return data as T;
        } catch (err: any) {
          clearTimeout(timeoutId);

          if (err.name === 'AbortError') {
            lastError = this.normalizeError({ message: `Request timeout exceeded (${timeoutMs}ms)` }, 408);
          } else if (err.status === 'error') {
            throw err;
          } else {
            lastError = this.normalizeError(err, 500);
          }

          if (attempt < retries) {
            await new Promise((r) => setTimeout(r, backoffMs * Math.pow(2, attempt)));
          }
        }
      }

      throw lastError;
    })();

    if ((fetchOptions.method || 'GET') === 'GET') {
      this.pendingRequests.set(requestKey, requestPromise);
      requestPromise.finally(() => this.pendingRequests.delete(requestKey));
    }

    return requestPromise;
  }

  get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  post<T>(endpoint: string, body: any, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(body),
    });
  }
}

export const apiClient = new EnterpriseApiClient();
