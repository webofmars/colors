FROM nginx

LABEL org.opencontainers.image.source https://github.com/webofmars/colors

ARG COLOR=red

COPY index.html /usr/share/nginx/html/index.html
RUN sed -i "s/__COLOR__/${COLOR}/g" /usr/share/nginx/html/index.html
