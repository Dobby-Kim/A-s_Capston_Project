# Step 1: Use the node image for building the React app
FROM node:latest as build

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json (or yarn.lock)
COPY app/package*.json ./

# Install dependencies
RUN npm install

# Step 4: Copy the React project files into the container
COPY app/ ./

# Step 5: Build the app
RUN npm run build

# Step 6: Use nginx to serve the app
FROM nginx:alpine

# Copy the build from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
