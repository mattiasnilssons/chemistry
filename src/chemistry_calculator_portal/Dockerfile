# Build stage for compiling the frontend assets
FROM node:18 as builder

# Set the working directory
WORKDIR /app

# Copy package management files to the working directory
COPY src/chemistry_calculator_portal/package.json src/chemistry_calculator_portal/package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the frontend codebase into the image
COPY src/chemistry_calculator_portal .

# Build the project
RUN npm run build

# Production image, copy all the files and run nginx
FROM nginx:stable-alpine

# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html

# Remove default nginx static assets
RUN rm -rf ./*

# Copy static assets from builder stage
COPY --from=builder /app/build .

# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]
