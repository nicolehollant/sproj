server {
        listen 80;
        server_name sproj.colehollant.com;

        location / {
                proxy_pass http://localhost:8080;
        }
}
