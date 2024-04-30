FROM node:16-buster-slim

WORKDIR /frontend

COPY package*.json ./

RUN rm -rf node_modules package-lock.json
RUN npm install @rollup/rollup-linux-x64-gnu --save-optional
RUN npm install react-dropzone

COPY . .

EXPOSE 6390

CMD ["npm", "run", "dev"]
