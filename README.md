# Automation Project Setup Guide

## Steps to Run the Automation Project

### Installations

#### Python
- Used with Python 3.8+
- Required for running test scripts
- [Download Python](https://www.python.org/downloads/)

#### Appium Server
- Version 2.0+ recommended
- Installation: `npm install -g appium`
- Requires Node.js (v14+)

#### Appium UiAutomator2 Driver
- Installation: `appium driver install uiautomator2`

#### Android SDK
- Minimum API level matching the app's minimum SDK
- Install via Android Studio or command line tools
- Required components:
  - Platform Tools
  - Build Tools
  - Platform SDK
  - Android Emulator

#### Java Development Kit (JDK)
- Version 8 or higher
- Required for Android tools
- Export environment variables to `.bash_profile`, `.zshrc`, or `.profile`:
  ```sh
  export ANDROID_HOME=/path/to/your/androidSDK 
  export PATH=$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$PATH
  export JAVA_HOME=/path/to/JDK
  export ANDROID_SDK_ROOT=/path/to/Android/sdk
  export PATH=$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/tools:$PATH
  ```

### Python Dependencies
- Install via pip after cloning the repository:
  ```sh
  pip install -r requirements.txt
  ```
- The `requirements.txt` includes:
  - appium-python-client
  - pytest
  - pytest-fixture-config
  - python-dotenv
  - feedparser

### Android Emulator Setup

#### Emulator
- Create via Android Studio's AVD Manager

#### Environment Setup
- Create `.env` file
- Copy from `.env.template`
- Configure with your specific settings:
  ```sh
  APPIUM_SERVER_URL="http://127.0.0.1:4723"
  ANDROID_APP_PATH="/path/to/news-app.apk"
  ANDROID_PLATFORM_NAME="Android"
  ANDROID_DEVICE_NAME="emulator-5554"  # or your device ID
  ANDROID_DEVICE_PLATFORM_VERSION="15"  # or your Android version
  AUTOMATOR="UiAutomator2"
  ```

### Test App Setup

#### News App APK
- Download the latest APK from: [News App Releases](https://github.com/bubelov/news/releases)
- Update `ANDROID_APP_PATH` in `.env` to point to the APK

### Optional Tools

#### Appium Inspector
- For element inspection and test development
- [Download Appium Inspector](https://github.com/appium/appium-inspector/releases)

#### Scrcpy (if using a real device)
- For device screen mirroring
- [Installation Guide](https://github.com/Genymobile/scrcpy)

#### Android Studio
- For emulator management and app inspection
- [Download Android Studio](https://developer.android.com/studio)

#### Appium Doctor
- Terminal tool for environment installation check

### Verification Steps
After installation, verify your setup:

#### Check Appium installation
```sh
appium --version
```

#### Check Android SDK installation
```sh
adb devices  # Should list connected devices/emulators
```

#### Check Python environment / Verify device connection
```sh
python --version
pip list  # Should show all required packages
```

#### Run Appium server
```sh
appium
```

### Running the Tests
Once everything is installed:

1. Start Appium server:
   ```sh
   appium
   ```

2. Start Android emulator or connect a device:
   ```sh
   emulator -avd [emulator_name]  
   ```
   Or connect a physical device
   Or start from device management in Android Studio

3. Run tests:
   ```sh
   cd /path/to/project
   pytest  # pytest should already run all tests as configured in pytest.ini
   pytest -s -v  # For more detailed outputs
   ```
