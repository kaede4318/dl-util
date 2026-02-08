// src/config/api.ts
const protocol = import.meta.env.VITE_API_PROTOCOL ?? "http";
const host = import.meta.env.VITE_API_HOST ?? window.location.hostname;
const port = import.meta.env.VITE_API_PORT ?? "8000";

export const API_BASE_URL = `${protocol}://${host}:${port}`;