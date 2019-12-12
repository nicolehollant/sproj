server {
        ssl on;
        ssl_certificate /path/to/my/public/certs;
        ssl_certificate_key /path/to/my/private/certs;
        listen 443 ssl;
        listen [::]:443 ssl;


        server_name sproj.colehollant.com;

        location / {
                proxy_pass http://localhost:8080;
        }
}

server {
        listen 80;
        server_name sproj.colehollant.com;
        return 301 https://$host$request_uri;
}