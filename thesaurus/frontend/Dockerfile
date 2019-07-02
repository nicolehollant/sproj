FROM node:10.9-slim as build-stage
RUN yarn global add @vue/cli -g
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN yarn install
RUN yarn build

FROM nginx:1.15.3
COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html/dist
RUN rm /etc/nginx/conf.d/default.conf
COPY  nginx.conf /etc/nginx/conf.d/app.conf
EXPOSE 80
WORKDIR /etc/nginx
CMD ["nginx", "-g", "daemon off;"]