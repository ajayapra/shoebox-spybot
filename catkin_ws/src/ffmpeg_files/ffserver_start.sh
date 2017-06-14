#The "ffserver -f /etc/ffserver.conf" starts the ffserver with the given configuration (check ffserver.conf)

#The "ffmpeg -v verbose -r 5 -s 300x240 -f video4linux2 -i /dev/video0 http://localhost:8090/feed1.ffm" creates an internal video stream from /dev/video0 (our camera) to localhost, which can then be picked by the ffserver feed, and then can be streamed by ffserver



ffserver -f /etc/ffserver.conf & ffmpeg -v verbose -r 5 -s 300x240 -f video4linux2 -i /dev/video0 http://localhost:8090/feed1.ffm
