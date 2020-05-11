server {
    listen 80 default_server;

    server_name mydomain.com www.mydomain.com;
    location / {
        proxy_pass http://localhost:8081;
    }

}