# VitalDocz Blog
Deployed at: https://blog.vitaldocz.com

## Dependencies

* Python 3.6
* VirtualEnv & VirtualEnv Wrapper
* MySQL

## Installation and running

* sudo mkdir blog
* cd blog
* git clone [https://github.com/Vitaldocz/blog.git](https://github.com/Vitaldocz/blog.git)
* sudo chmod 700 -R ./
* mysql -u {root-user} -p < ./db_settings.sql
* ./installer.sh

Open Browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000)