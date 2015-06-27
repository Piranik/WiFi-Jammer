# Android-WiFi-Jammer
Application using aircrack-ng suite packet to jam wifi signal

#USING ON RASPBERRY PI:

sudo apt-get update

sudo apt-get upgrade

sudo apt-get dist-upgrade 

sudo  apt-get install libnl-dev libssl-dev iw

wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc2.tar.gz

tar -zxf aircrack-ng-1.2-rc2.tar.gz

cd aircrack-ng-1.2-rc2.tar.gz

make

sudo make install

sudo airodump-ng-oui-update

cd .. 

rm -rf aircrack-ng*
