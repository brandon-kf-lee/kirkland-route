// src/api.js
const apiBaseUrl = process.env.NODE_ENV === 'development'
  ? 'http://localhost:5000' 
  : 'https://kirkland-route-production.up.railway.app';

export default apiBaseUrl;