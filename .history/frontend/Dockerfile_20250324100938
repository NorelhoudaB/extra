FROM node:18

WORKDIR /frontend

COPY package*.json ./

RUN npm install

 #RUN npm install bootstrap bootstrap-icons

COPY . .
 
ENV PORT=5173

EXPOSE 5173

CMD ["npm", "run", "dev"]
