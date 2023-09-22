FROM nginx:1.18
RUN rm -rf /usr/share/nginx/*
RUN mkdir /usr/share/nginx/html
COPY index.html /usr/share/nginx/html/
COPY register.html /usr/share/nginx/html/
COPY register.js /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/
