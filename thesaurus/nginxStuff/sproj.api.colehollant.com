server {
        listen 80;
        server_name sproj.api.colehollant.com;

        location / {
                proxy_pass http://localhost:3000;
        }
}
