FROM node:18 as builder
LABEL authors="Mattias"

ARG VITE_WEBSITE_HOST
ENV VITE_WEBSITE_HOST=$VITE_WEBSITE_HOST

ARG VITE_BACKEND_HOST
ENV VITE_BACKEND_HOST=$VITE_BACKEND_HOST

ARG VITE_FIREBASE_API_KEY
ENV VITE_FIREBASE_API_KEY=$VITE_FIREBASE_API_KEY

ARG VITE_FIREBASE_AUTH_DOMAIN
ENV VITE_FIREBASE_AUTH_DOMAIN=$VITE_FIREBASE_AUTH_DOMAIN

COPY package.json src/chemistry_calculator_portal/package-lock.json /tmp/
RUN cd /tmp \
    && npm install

COPY ./src/chemistry_calculator_portal /tmp/
RUN cd /tmp \
    && npm run build

FROM node:18-alpine

ARG ORIGIN
ENV ORIGIN=$VITE_WEBSITE_HOST

WORKDIR /app
COPY --from=builder /tmp/build /app
COPY --from=builder /tmp/package.json /app/
CMD ["node", "index.js"]
