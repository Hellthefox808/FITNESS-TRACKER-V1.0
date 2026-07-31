/**
 * Enterprise Telemetry Stream Service
 * Manages WebSocket connections for 1 Hz biometric streaming,
 * handling automatic heartbeats and exponential reconnect backoff.
 * Author: Ravi Ranjan Singh
 */

export interface TelemetryFrame {
  heart_rate_bpm: number;
  body_temp_c: number;
  weight_kg: number;
  age: number;
  gender: string;
  duration_min: number;
}

export interface BurnVelocityUpdate {
  event: string;
  current_heart_rate_bpm: number;
  burn_rate_kcal_per_min: number;
  cumulative_calories: number;
  intensity_zone: string;
}

export class TelemetryStreamService {
  private wsUrl: string;
  private socket: WebSocket | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private listeners: Array<(data: BurnVelocityUpdate) => void> = [];

  constructor(wsUrl: string = 'ws://localhost:8000/ws/v1/telemetry') {
    this.wsUrl = wsUrl;
  }

  connect(token?: string): void {
    const url = token ? `${this.wsUrl}?token=${token}` : this.wsUrl;
    try {
      this.socket = new WebSocket(url);

      this.socket.onopen = () => {
        this.reconnectAttempts = 0;
      };

      this.socket.onmessage = (event) => {
        try {
          const data: BurnVelocityUpdate = JSON.parse(event.data);
          this.listeners.forEach((listener) => listener(data));
        } catch {
          /* ignore parse errors */
        }
      };

      this.socket.onclose = () => {
        this.handleReconnect(token);
      };

      this.socket.onerror = () => {
        if (this.socket) {
          this.socket.close();
        }
      };
    } catch {
      this.handleReconnect(token);
    }
  }

  private handleReconnect(token?: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const timeout = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      setTimeout(() => this.connect(token), timeout);
    }
  }

  sendTelemetry(frame: TelemetryFrame): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ event: 'TELEMETRY_FRAME', ...frame }));
    }
  }

  subscribe(listener: (data: BurnVelocityUpdate) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export const telemetryStreamService = new TelemetryStreamService();
