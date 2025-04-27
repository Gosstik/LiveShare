export const ENV = {
  BACKEND_BASE_URL: process.env.REACT_APP_BACKEND_BASE_URL || 'http://localhost:8000',
  ACCESS_TOKEN_BUFFER_SEC: Number(process.env.REACT_APP_ACCESS_TOKEN_BUFFER_SEC) || 30,
};
