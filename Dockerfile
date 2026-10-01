FROM node:20-slim

WORKDIR /app

COPY package.json tsconfig.json index.js ./

RUN npm install --omit=dev

COPY scripts ./scripts
COPY src ./src

EXPOSE 8080
ENV PORT=8080

CMD ["node", "index.js"]
