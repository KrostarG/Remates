# build.sh
#!/bin/bash
set -e

# Otorgar permisos de ejecución al propio script
chmod +x build.sh
# Leer e instalar los paquetes del archivo apt-packages
if [ -f "apt-packages" ]; then
  apt-get update
  xargs apt-get install -y < apt-packages
fi


# Instalar Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Instalar las bibliotecas ODBC necesarias
apt-get install -y unixodbc unixodbc-dev

# Instalar ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip -d /usr/local/bin/
rm /tmp/chromedriver.zip

# Instalar las dependencias de Python
pip install -r requirements.txt
