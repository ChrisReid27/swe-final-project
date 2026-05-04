const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    credentials: 'include',
    ...options,
  });

  const contentType = response.headers.get('content-type') ?? '';
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message = typeof payload === 'string'
      ? payload
      : payload?.detail ?? 'Request failed';
    throw new Error(message);
  }

  return payload;
}

export function createGameboard() {
  return request('/game/');
}

export function getGameboard(boardCode) {
  return request(`/game/${boardCode}/`);
}

export function getLeaderboard(boardCode) {
  return request(`/games/${boardCode}/leaderboard/`);
}

export function submitLeaderboard(boardCode, data) {
  return request(`/games/${boardCode}/leaderboard/`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}