# install_dependencies.sh
#!/bin/bash

# Actualizar los paquetes
apt-get update

# Instalar las bibliotecas ODBC necesarias
apt-get install -y unixodbc unixodbc-dev

# Limpiar el caché de apt
apt-get clean
