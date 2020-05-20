FROM mhart/alpine-node

WORKDIR usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY . /usr/src/app/

RUN npm install

EXPOSE 3000
CMD ["npm", "run", "dev"]
