#!/bin/bash
gst-launch-1.0 -v v4l2src device=/dev/video0  \
! "image/jpeg,width=1280, height=720,framerate=30/1" \
! rtpjpegpay \
! udpsink host=192.168.86.248 port=5000
