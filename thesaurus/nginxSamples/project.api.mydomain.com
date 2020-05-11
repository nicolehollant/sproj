server {
        listen 80;
        server_name project.api.mydomain.com;

        location / {
                proxy_pass http://localhost:3000;
        }
}
