# Use a specific version of node as the base image for the builder stage
FROM node:18 as builder

# Set working directory to ensure that all paths in subsequent commands are relative to this location
WORKDIR /app

# Copy package.json and package-lock.json for npm install
COPY src/chemistry_calculator_portal/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your frontend codebase into the image
COPY src/chemistry_calculator_portal/ .

# Build the project (assuming a script named 'build' exists in package.json)
RUN npm run build

# Use a specific version of node for the production stage
FROM node:18-alpine

# Set working directory for the production image
WORKDIR /app

# Copy the build directory from the builder stage to the production image
COPY --from=builder /app/build /app

# Specify Node.js to treat .js files as modules
ENV NODE_OPTIONS="--experimental-modules"

# Set environment variables for the runtime
ARG VITE_WEBSITE_HOST
ENV VITE_WEBSITE_HOST=$VITE_WEBSITE_HOST
ARG VITE_BACKEND_HOST
ENV VITE_BACKEND_HOST=$VITE_BACKEND_HOST
ARG VITE_FIREBASE_API_KEY
ENV VITE_FIREBASE_API_KEY=$VITE_FIREBASE_API_KEY
ARG VITE_FIREBASE_AUTH_DOMAIN
ENV VITE_FIREBASE_AUTH_DOMAIN=$VITE_FIREBASE_AUTH_DOMAIN
ARG ORIGIN
ENV ORIGIN=$VITE_WEBSITE_HOST

# Start the application
CMD ["node", "--experimental-modules", "index.js"]
