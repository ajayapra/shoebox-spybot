# shoebox-spybot
A RaspberryPi + Arduino based spybot
![picture](https://raw.githubusercontent.com/ajayapra/shoebox-spybot/master/shoebox-spybot.jpg "Shoebox Spybot!!")
## Useful links
  - [ROS + UBUNTU MATE](http://www.german-robot.com/2016/05/26/raspberry-pi-sd-card-image/)
  - [RUFUS, for burning img/iso files and creating bootable disks](https://rufus.akeo.ie/)
  - [Ubuntu GNOME](https://wiki.ubuntu.com/UbuntuGNOME/GetUbuntuGNOME)
  - [Install UBUNTU on USB](http://ubuntuhandbook.org/index.php/2014/11/install-real-ubuntu-os-usb-drive/)
  - [HowTo: Configure VNC on RasPi](https://www.realvnc.com/docs/raspberry-pi.html#raspberry-pi-ssh)
  - [HowTo: Install Arduino on Ubuntu](https://www.arduino.cc/en/Guide/Linux)
  - [`rosserial_arduino`: Interface Arduino with ROS](http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup)

## Commands
  - `robot`: Starts the camera feed and keyboard control on the bot. View the feed at http://pi-desktop:8090/test.mjpg once you've configured `pi-desktop` in */etc/hosts*. Press `q` to exit.
  - `robot-cam`: Starts only the camera feed and the serial comm nodes. To be used in combination with `robot-remote` and after opening an SSH connection to `pi-desktop` to control and move the robot from another computer
  - `robot-remote`: Starts the control node, and sets the ROS IP to the Raspberry Pi on the remote computer
  - `robot-force`: Enables object tracking "force-mode" on the robot. Press `v` to pause, and `q` to quit.
  - `execme.sh` : Script that copies all these custom commands to *~/bin* and adds the path to the executable paths.
  
## Progress log
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
  
- **06/16/17**
  - Started work on the Arduino.
  - Arduino IDE from *Software* (snap app) did not work.
  - Downloaded and installed Arduino IDE following instructions [here](https://www.arduino.cc/en/Guide/Linux)
  - `install.sh` did not work, use [this](https://github.com/ajayapra/shoebox-spybot/blob/master/catkin_ws/src/arduino_installer/install.sh) file instead. 
  - Add `--novendor` option to all the `xdg` commands to prevent errors.
  - Run `sudo chmod +777 /dev/ttyACM0` on whichever port the Arduino is connected to, to enable code burning.
  - Check port permissions using `ls -la /dev/tyACM0`
  - Created Arduino workspace
  - Lesson Learned: Do not delete the Arduino folder used to install the IDE. The IDE does not copy itelf over, instead it runs out of this folder itself.
  - PROTIP: Change the name of the folder and copy it somewhere else from *~/Downloads*, making updating easier, and so that its not deleted by accident.
  - Redirect Arduino sketchbook folder from preferences to */home/$USER/shoebox-spybot/arduino_ws*
  - Add user to the dialout group to enable serial write on the arduino permanently `sudo usermod -a -G dialout $USER`
  - Installed `rosserial_arduino` following instructions above
  - Finished the bot_driver Arduino code.
  - Need to run `rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=57600` to start transmitting to Arduino
  - Burn the [*bot_driver.ino*](https://github.com/ajayapra/shoebox-spybot/blob/master/arduino_ws/bot_driver/bot_driver.ino) sketch to start driving the bot around
  - Rinse-Repeat these steps on the RasPi
 
 - **06/16/17**
   - Last day of the self-set one week deadline for this build.
   - Made `comm.launch`, that'll help launch `rosserial_python`
   - Made `teleop.launch`, to launch the teleop node
   - TIP: add `output=screen` to the XML tag of the node you want displayed in the foreground
   - Created custom shell commands `robot`, `robot-cam`, and `robot-remote` to make it easier to launch the program via CLI
   - Add `export PATH=$PATH:~/bin` to *~/.bashrc* to use these custom shell commands from the terminal
   - Run `./catkin_ws/Bash/execme.sh` to create copies of the custom shell commands in *~/bin* folder
   - Documentation on how these commands work found [here](https://github.com/ajayapra/shoebox-spybot/blob/master/catkin_ws/src/Bash/robot)
   - OPTIONAL: This is how you set a default login for the CLI interface:
     - `sudo pluma etc/systemd/system/getty.target.wants/getty@tty1.service`.
     - Under `[Service]` , Find line that says `ExecStart=-/sbin/agetty --noclear %I $TERM`.
     - Change it to `ExecStart=-/sbin/agetty --noclear -a <user> %I $TERM` where `<user>` is your username.
     - Reboot and CLI should autologin to `<user>`.
     - Useful if you just want to execute the commands without a screen and want the robot moving.
   - That marks the end of the initial stage of this project. Will be including OpenCV image processing stuff next week.
       
- **06/17/17**
  - Cloned and modified object tracking algorithm from a [previous project](https://github.com/amkurup/object_trcaking)
  - To change keyboard layouts (since the UBUNTU+ROS image comes with all kinds of German settings) run `sudo dpkg-reconfigure keyboard-configuration`
  - Created a control node, which can be called by the command `robot-force`, Tracking can then be enabled/disabled by pressing `v`. Press `q` ro quit
