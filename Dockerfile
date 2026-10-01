FROM node:20-slim

WORKDIR /app

COPY package.json tsconfig.json index.js ./
RUN npm install --omit=dev

COPY scripts ./scripts
COPY src ./src

ENV PORT=10000
EXPOSE 10000

CMD ["node", "index.js"]
