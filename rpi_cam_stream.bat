@echo off
cd C:\gstreamer\1.0\mingw_x86_64\bin
gst-launch-1.0 -e -v udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink