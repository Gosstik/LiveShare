// Docs on how to create and use env variables:
// https://create-react-app.dev/docs/adding-custom-environment-variables/

// env file is choosing depending on NODE_ENV variable.
// NODE_ENV is set in the following way:

// npm start => 'development'
// npm test => 'test'
// npm run build => 'production'

export const ENV = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  BACKEND_BASE_URL: process.env.REACT_APP_BACKEND_BASE_URL || 'http://localhost:8000',
  ACCESS_TOKEN_BUFFER_SEC: Number(process.env.REACT_APP_ACCESS_TOKEN_BUFFER_SEC) || 30,
};
