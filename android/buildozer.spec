[app]

# Application title
title = TarotMac Android

# Package name
package.name = tarotmac

# Package domain (unique identifier)
package.domain = com.tarotmac.android

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# Application version
version = 1.0.0

# Application requirements
requirements = python3,kivy==2.2.0,kivymd==1.1.1,pydantic==2.5.0,sqlalchemy==2.0.23,cryptography==41.0.7,ollama==0.1.7,plyer==2.1.0,pyjnius==1.4.2

# Android specific
[android]

# Android API level
api = 33

# Minimum Android API level
minapi = 21

# Android SDK version
sdk = 33

# Android NDK version
ndk = 25b

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Application icon
icon.filename = assets/icon.png

# Application presplash
presplash.filename = assets/presplash.png

# Orientation
orientation = portrait

# Fullscreen mode
fullscreen = 0

# Debug mode
debug = 1

# Log level
log_level = 2

# Build configuration
[buildozer]

# Log level
log_level = 2

# Warn on error
warn_on_root = 1