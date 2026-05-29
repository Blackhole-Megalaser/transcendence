FROM node:22-alpine AS node-build-stage
WORKDIR /app
COPY ./vue/package*.json ./
RUN npm ci
COPY ./vue/ ./
RUN npm run build

FROM alpine/openssl AS ssl-build-stage
WORKDIR /app
RUN openssl ecparam -genkey -out ecdsakey.pem -name prime256v1
RUN openssl req -x509 -noenc -new -key ecdsakey.pem -out ./cat.crt -keyout ./cat.key -subj "/C=FR/ST=Normandie/L=Le_Havre/O=42/OU=42/CN=hacker-cat/UID=TheCatCommittee"


FROM nginx:stable-alpine AS production-stage
COPY --from=node-build-stage /app/dist /usr/share/nginx/html
COPY --from=ssl-build-stage /app/ /etc/nginx/ssl
COPY ./vue/src/assets/favicon.ico /usr/share/nginx/html/favicon.ico
COPY /nginx/nginx.conf /etc/nginx/conf.d/default.conf.template
COPY ./entrypoint.sh /app/entrypoint.sh

EXPOSE 443
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
