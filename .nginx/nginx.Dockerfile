FROM nginx:alpine-slim

COPY /.nginx/default.conf /etc/nginx/nginx.conf

EXPOSE 80