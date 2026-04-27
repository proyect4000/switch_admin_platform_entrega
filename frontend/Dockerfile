FROM node:20-alpine
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --no-frozen-lockfile
COPY . .
EXPOSE 5173
CMD ["pnpm", "vite", "--mode", "base", "--host", "0.0.0.0"]
