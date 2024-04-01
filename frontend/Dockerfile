FROM node:lts-alpine
WORKDIR /app
# install dependencies so this layer can be cached by docker when dependencies don't change
COPY package*.json ./
RUN npm install
RUN npm install -g http-server
COPY . .
# build app for production
RUN npm run build
EXPOSE 8080
# serve content
CMD [ "http-server", "dist" ]
