FROM alpine:3.21

# Install nginx
RUN apk add --no-cache nginx && \
        rm -rf /etc/nginx/* \
        touch /run/nginx.pid

COPY conf/* /etc/nginx/

# Creating user
RUN addgroup -g 1000 -S nginx_group && \
    adduser -u 1000 -S nginx_user -G nginx_group && \
    chown -R nginx_user:nginx_group \
        /var/lib/nginx \
        /var/log/nginx \
        /run/nginx.pid
USER nginx_user

EXPOSE 80

# Run nginx on foreground to prevent container exit
CMD ["nginx", "-g", "daemon off;"]
