FROM node:23.11.0

WORKDIR /code

COPY package*.json ./

RUN npm install

#RUN npm install bootstrap bootstrap-icons

COPY . /code
 
ENV PORT=8911
ENV HOST=0.0.0.0

EXPOSE 8911


CMD ["npm", "run", "dev"]
