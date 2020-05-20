FROM mhart/alpine-node

WORKDIR usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json

RUN yarn install
RUN yarn build

EXPOSE 3000
CMD ["yarn", "start"]
