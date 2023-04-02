#!/bin/bash

set -e

cd ~ || exit

sudo apt-get -y install redis-server libcups2-dev -qq

pip install dontmanage-bench

git clone https://github.com/dontmanage/dontmanage --branch "$BRANCH_TO_CLONE" --depth 1
bench init --skip-assets --dontmanage-path ~/dontmanage --python "$(which python)" dontmanage-bench

mkdir ~/dontmanage-bench/sites/test_site
cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config.json" ~/dontmanage-bench/sites/test_site/

mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'"
mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_dontmanage'@'localhost' IDENTIFIED BY 'test_dontmanage'"
mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_dontmanage"
mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_dontmanage\`.* TO 'test_dontmanage'@'localhost'"

mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'"
mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES"

install_whktml() {
    wget -O /tmp/wkhtmltox.tar.xz https://github.com/dontmanage/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
    sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
    sudo chmod o+x /usr/local/bin/wkhtmltopdf
}
install_whktml &

cd ~/dontmanage-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app payments
bench get-app https://github.com/dontmanage/dontmanageerp --branch "$BRANCH_TO_CLONE" --resolve-deps
bench setup requirements --dev

bench start &> bench_run_logs.txt &
CI=Yes bench build --app dontmanage &
bench --site test_site reinstall --yes

bench get-app hrms "${GITHUB_WORKSPACE}"
bench --site test_site install-app hrms
bench setup requirements --dev