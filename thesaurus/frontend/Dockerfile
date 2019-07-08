FROM node:lts-alpine as build-stage
WORKDIR /app
COPY . .
RUN yarn global add @vue/cli -g
RUN yarn install
RUN yarn build


FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
