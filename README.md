# 2073-jevois-vision-suite

FIRST Team 2073 Vision Tracking using JeVois

During the off season in 2017, Team 2073 experimented with the JeVois Smart camera to determine if it would be a reasonable replacement for the Raspberry Pi 3 paired with a Lifecam HD-3000 that has been used for the last couple of seasons. It was quickly found that the JeVois was a very capable and powerful camera and more than met our expectations.

With that, we embarked on creating a [White Paper](https://www.chiefdelphi.com/media/papers/3405) that can be downloaded from Chief Delphi. This paper should be followed prior to trying to implement our code.

With the release of our vision tracking code, you should be able to get target tracking working in just a couple hours. This will not be quite as plug and play as the $400 Limelight, but by following the White Paper and using this code, it will be close.

In this package you will find four pieces of code: 

**EagleTuner.py**-
The first is run on a separate PC and is used to send tuning values to the camera. **This script requires you use Python 2.7 on the hosting device.**
 *(Make sure to edit this code to use the "COM Port" your PC has detected the JeVois is connected to.)*

**EagleTrackCal.py**-
The second is used with the first. It runs on JeVois and is the code that receives the commands and sets the calibration values. The output of the code is a simple binary image to help guide your adjustments. It also writes the calibration values to a file on JeVois. This is launched via AMCap. “MJPG 320X240 30fps”


**EagleTracker.py**-
The third is used to validate the calibrations and create tracking values to be sent out serially to the roboRio. It uses the calibration values that were written to the “Calibration” file. This is launched via AMCap. “MJPG 320X240 15fps”


**EagleTrkNoStream.py**-
The last script is the one that actually runs during matches. It too uses the “Calibration” file for it’s tuning parameters. Unlike the third file, it does not stream video. Thus, it needs to be initiated by a line in “initscript.cfg”.

If you would like to be a contributor to this repo, please contact me though a private message on Chief Delphi. My user name there is [Billbo911](https://www.chiefdelphi.com/forums/member.php?u=10773).


