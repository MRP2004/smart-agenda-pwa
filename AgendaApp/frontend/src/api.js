const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function request(path, { method = 'GET', body, token, headers = {} } = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || 'API request failed');
  }

  if (response.status === 204) return null;
  return response.json();
}

export const loginRequest = async (email, password) => {
  const formData = new URLSearchParams({ username: email, password });
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData,
  });

  if (!response.ok) throw new Error('Invalid credentials');
  return response.json();
};
