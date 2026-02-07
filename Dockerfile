# Multi-stage build for frontend and backend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Backend stage
FROM python:3.9-slim AS backend

WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Production stage
FROM nginx:alpine

# Copy frontend build
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html

# Copy backend (optional - for API)
COPY --from=backend /app/backend /app/backend

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
