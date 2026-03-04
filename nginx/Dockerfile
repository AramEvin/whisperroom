FROM nginx:alpine

# Bake config into image — no volume mount needed
COPY whisperroom.conf /etc/nginx/conf.d/default.conf

# Remove default nginx config
RUN rm -f /etc/nginx/conf.d/default.conf.bak

EXPOSE 80
