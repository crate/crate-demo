## -*- docker-image-name: "clma/eden" -*-
FROM stephank/archlinux:armv6-latest
MAINTAINER clma <claus.matzinger+kb@gmail.com>

RUN pacman -Sy --noconfirm git opencv python3 python-pip python3-numpy  && pacman -Sc --noconfirm
RUN mkdir /eden && git clone https://github.com/celaus/picam.demo.git eden && cd /eden && python setup.py install
ENV LD_LIBRARY_PATH /eden
WORKDIR /eden
CMD ["capture"]
