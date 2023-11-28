# Use the official Node.js 14 image as a parent image
FROM node:14

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any dependencies
RUN npm install

# Copy the rest of your app's source code
COPY . ./

# Expose port 3000
EXPOSE 3000

# Run the application
CMD ["node", "server.js"]
