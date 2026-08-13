// Extract API base URL from Vite environment, fallback to localhost for development
const env = (import.meta as unknown as { env: Record<string, string> }).env;
export const API_BASE_URL = env?.VITE_API_BASE_URL || 'http://localhost:8000';

export function getWebSocketUrl(path: string): string {
  // Ensure path starts with a slash
  const safePath = path.startsWith('/') ? path : `/${path}`;
  
  // Convert http:// to ws:// and https:// to wss://
  const wsBase = API_BASE_URL.replace(/^http:\/\//i, 'ws://').replace(/^https:\/\//i, 'wss://');
  
  return `${wsBase}${safePath}`;
}
