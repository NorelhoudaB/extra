FROM node:18

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .
 
ENV PORT=5173

EXPOSE 80 5679

CMD ["npm", "run", "dev"]
