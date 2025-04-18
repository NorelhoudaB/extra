FROM node:23.11.0

WORKDIR /code

COPY package*.json ./

RUN npm install
RUN npm install -g serve

#RUN npm install bootstrap bootstrap-icons

COPY . /code
 
ENV HOST=0.0.0.0

EXPOSE 8911


CMD serve -s dist -l tcp:$PORT