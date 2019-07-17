# Install and start Nginx
sudo apt install nginx
sudo systemctl start nginx
# configure server blocks
sudo vim /etc/nginx/sites-available/colehollant.com
sudo vim /etc/nginx/sites-available/sproj.colehollant.com
sudo vim /etc/nginx/sites-available/sproj.api.colehollant.com
# enable them
sudo ln /etc/nginx/sites-available/sproj.colehollant.com /etc/nginx/sites-enabled/sproj.colehollant.com
sudo ln /etc/nginx/sites-available/sproj.api.colehollant.com /etc/nginx/sites-enabled/sproj.api.colehollant.com
# check syntax and reload
sudo nginx -t 
sudo systemctl reload nginx


# MAKE SURE THAT YOU'VE SET UP A RECORDS ON DIGITALOCEAN AND GOOGLE LOLL