server {
    listen 80 default_server;

    server_name colehollant.com www.colehollant.com;
    location / {
        proxy_pass http://localhost:8081;
    }

}