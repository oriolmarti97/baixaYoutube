#!/bin/bash


if [ -x "$(command -v apt)" ]; then
	apt install python3 python3-pip
elif [ -x "$(command -v pacman)" ]; then
	pacman -S python3 python3-pip
elif [ -x "$(command -v yum)" ]; then
	yum install python3 python3-pip
else 
	echo "Gestor de paquets no detectat!"
	echo "Instal·la manualment python3 i el pip i executa les següents comandes"
	echo "pip3 install youtube-dl"
	echo "pip3 install PyQt5"
	exit
fi

pip3 install youtube-dl PyQt5

if [[ $# -lt 1 ]]; then
	echo "Instal·lant a la ubicació predeterminada"
	mv baixaYoutube.py /usr/bin/baixaYoutube
else
	echo "Instalant a la ubicacio $1"
	mv baixaYoutube.py $1/baixaYoutube
fi


