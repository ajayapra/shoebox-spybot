# shoebox-spybot
A RaspberryPi + Arduino based spybot
## Useful links
  - [ROS + UBUNTU MATE](http://www.german-robot.com/2016/05/26/raspberry-pi-sd-card-image/)
  - [Ubuntu GNOME](https://wiki.ubuntu.com/UbuntuGNOME/GetUbuntuGNOME)
  - [Install UBUNTU on USB](http://ubuntuhandbook.org/index.php/2014/11/install-real-ubuntu-os-usb-drive/)
  - [HowTo: Configure VNC on RasPi](https://www.realvnc.com/docs/raspberry-pi.html#raspberry-pi-ssh)
  - [HowTo: Install Arduino on Ubuntu](https://www.arduino.cc/en/Guide/Linux)

# Progress log
- **06/12/17**: 
  - Installed UBUNTU MATE + ROS on the Raspberry. 
  - Reinstalled UBUNTU GNOME 16.04 and ROS on the laptop. 
  - Configured VNC. 
  - Made this repository. 
  - Created base workspace. 
  - Created remote sourcing bash script (may need work as ROS_IP is being set blank). 
  - Tested remote sourcing bash script; works. 
  - Cloned and synced workspaces in both machines.   

- **06/13/17**
  - Created a simple teleop publisher to the *turtlesim_node*. Needs tuning to be used with the real robot.
  - Made a base level *action_input* wrapper to wrap around keyboard inputs.
  - Echoed commands from PC nodes to move the *turtlesim_node* running on the Raspberry Pi
  - As initially suspected, ROS_IP was being set blank, and this caused problems
  - Easily fixed, by replacing `wlan0` in the shellscript with `wlp2s0`
  - All of today's code resides in the *teleop_test* package
  - Made a *teleop_final* node which is a modified fork of *key_teleop* from the official *ros-kinetic-teleop-tools* 

- **06/14/17**
  - Connected the camera to Raspberry Pi. Bad framerate. Trying to get 10 fps @ 320x240.
  - Default *cheese* configurations wont work. Set resolution manually from preferences.
  - Stumbled upon another interesting detail, UBUNTU MATE's spftware update utility is bugged
  - To update software on the Raspberry pi run `sudo apt update && sudo apt upgrade` and `sudo rpi-update`
  - Creating a shellscript for *ffserver*, so that the video feed can be accessed via browser from anywhere

- **06/15/17**
  - Built ffmpeg from scratch following instructions found [here](https://ubuntu-mate.community/t/tutorial-build-or-download-ffmpeg-libavcodec-with-mmal-support-hardware-acceleration-video-decoding/3565). Not required, but oh well, maybe it'll speed things up! NOTE: Takes time!! Binge watch all the things!!
  - Had a persistent error with *libavutil.so.55*, with the file disappearing/not being recognized.
  - Fixed by `sudo apt-get install libavutil\*` and by looking at the error path shown (*/usr/lib* in this case) and pasting the files there.
  - Tried a lot of configs for ffserver, and finally found one that works. 15 fps video stream achieved
  - Today's knowledge is contained within this [README](https://github.com/ajayapra/shoebox-spybot/blob/master/catkin_ws/src/ffmpeg_files/README) file.
  
- **06/13/17**
  - Started work on the Arduino.
  - Arduino IDE from *Software* (snap app) did not work.
  - Downloaded and installed Arduino IDE following instructions [here](https://www.arduino.cc/en/Guide/Linux)
  - `install.sh` did not work, use this file instead. Add `--novendor` option to all the `xdg` commands to prevent errors
  - Run `sudo chmod +777 /dev/ttyACM0` or whichever port the Arduino is coneected to, to enable code burning.
