#!/bin/sh

rm -rf pycacic
mkdir -p pycacic/DEBIAN pycacic/usr/share/ pycacic/usr/share/applications pycacic/etc/xdg/autostart pycacic/etc/cron.hourly pycacic/etc/init.d
mkdir pycacic/etc/rc2.d pycacic/etc/rc3.d pycacic/etc/rc4.d pycacic/etc/rc5.d

cp control pycacic/DEBIAN
cp postinst pycacic/DEBIAN
cp prerm pycacic/DEBIAN
cp postrm pycacic/DEBIAN
cp -a /usr/share/pycacic pycacic/usr/share
rm -f pycacic/cacic2.dat pycacic/logs/*.log
find pycacic -iname *.pyc | xargs rm -f
cp /usr/share/applications/pycacic.desktop pycacic/usr/share/applications/pycacic.desktop
cp /etc/xdg/autostart/pycacic.desktop pycacic/etc/xdg/autostart/pycacic.desktop
cp /etc/cron.hourly/chksis pycacic/etc/cron.hourly/chksis
cp /etc/init.d/cacic pycacic/etc/init.d/cacic


chown -R root:root pycacic/
chmod -R 0755 pycacic/DEBIAN/*

nome=PyCACIC_0.0.1.@revision@.deb
dpkg-deb -b pycacic /tmp/$nome
echo "Gerado pacote .deb em: /tmp/$nome"







