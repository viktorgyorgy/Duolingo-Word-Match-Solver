# Duolingo Word Match Solver
A script which solves the Match Madness event in Duolingo. Written with **python** and **appium**.  
<img width="300px" src="https://github.com/ViktorGyorgy/Duolingo-Word-Match-Solver/blob/main/recordings/short_showcase_small.gif"/> 

# What the script does
- The script runs on a computer, and solves the minigame on a phone connected to the pc.
- It boots up the Duolingo on the phone, and plays Match Madness a number of times (the value of how many round are played can be changed in the config file).
- The code learns the word pairs during the gameplay. It can learn them for any language combination.
- The learned pairs are saved and loaded for later uses.
- The hardest level of match madness is solved with around 40 seconds remaining (for reference I have around 25% completion rate, and when I finish I have 5 second left).
- A full demonstration can be found in the recordings folder, named as "long_showcase.mp4".

# Setup
## Appium
Installation guide: [http://appium.io/docs/en/latest/quickstart/requirements](http://appium.io/docs/en/latest/quickstart/requirements).

## Python
It can be downloaded at [https://www.python.org/](https://www.python.org/).  
After installation run: ```pip install Appium-Python-Client```.

## Phone
1. Enable developer mode (https://developer.android.com/studio/debug/dev-options#enable).
2. At developer options, enable these settings: USB Debugging, USB debugging (Security setting), Don't lock screen.
3. Connect phone to pc

# How to run
1. Connect phone to pc via USB.
2. Check that the phone is connected. Run ```adb devices``` in a terminal (adb location by default is C:/Users/<username>/AppData/Local/Android/SDK/platform-tools/adb). There should be a device ID present, if the phone can be seen.
3. Run ```adb shell pm grant com.appindustry.everywherelauncher android.permission.WRITE_SECURE_SETTINGS``` (only needed at first run, at second or later runs not needed).
4. Run ```appium``` in a terminal.
5. In the project folder,  run ```python script.py```.
