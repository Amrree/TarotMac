# Android Build Instructions

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu/Debian recommended)
- **Python**: 3.10 or higher
- **Memory**: At least 8GB RAM
- **Storage**: At least 10GB free space
- **Internet**: Required for downloading dependencies

### Required Software
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y libjpeg-dev libpng-dev libfreetype6-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev
sudo apt install -y libsdl2-ttf-dev libportmidi-dev libswscale-dev
sudo apt install -y libavformat-dev libavcodec-dev zlib1g-dev

# Install Java Development Kit
sudo apt install -y openjdk-11-jdk

# Install Android SDK and NDK
sudo apt install -y android-sdk android-sdk-platform-tools
sudo apt install -y android-sdk-build-tools
```

### Python Dependencies
```bash
# Install Python packages
pip install --break-system-packages buildozer
pip install --break-system-packages cython
pip install --break-system-packages setuptools
```

## Build Process

### 1. Environment Setup
```bash
# Navigate to Android project directory
cd /workspace/android

# Set up environment variables
export PATH=$PATH:/home/ubuntu/.local/bin
export ANDROID_HOME=/usr/lib/android-sdk
export ANDROID_NDK_HOME=/usr/lib/android-sdk/ndk/25.0.8775105
```

### 2. Buildozer Configuration
```bash
# Initialize buildozer (if not already done)
buildozer init

# Edit buildozer.spec if needed
nano buildozer.spec
```

### 3. Build APK

#### Debug Build
```bash
# Build debug APK
buildozer android debug

# Output: bin/tarotmac-debug.apk
```

#### Release Build
```bash
# Build release APK
buildozer android release

# Output: bin/tarotmac-release.apk
```

### 4. Clean Build
```bash
# Clean build artifacts
buildozer android clean

# Clean and rebuild
buildozer android clean
buildozer android debug
```

## Build Configuration

### buildozer.spec Key Settings
```ini
[app]
title = TarotMac Android
package.name = tarotmac
package.domain = com.tarotmac.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

requirements = python3,kivy==2.2.0,kivymd==1.1.1,pydantic==2.5.0,sqlalchemy==2.0.23,cryptography==41.0.7,ollama==0.1.7,plyer==2.1.0,pyjnius==1.4.2

[android]
api = 33
minapi = 21
sdk = 33
ndk = 25b
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
icon.filename = assets/icon.png
presplash.filename = assets/presplash.png
orientation = portrait
fullscreen = 0
debug = 1
```

## Troubleshooting

### Common Issues

#### 1. Missing Dependencies
```bash
# Error: Cython not found
pip install --break-system-packages cython

# Error: setuptools not found
pip install --break-system-packages setuptools

# Error: Android SDK not found
sudo apt install -y android-sdk
```

#### 2. Build Failures
```bash
# Clean and rebuild
buildozer android clean
buildozer android debug

# Check buildozer.spec syntax
buildozer android debug --verbose
```

#### 3. Permission Issues
```bash
# Fix file permissions
chmod +x buildozer
chmod -R 755 .
```

#### 4. Memory Issues
```bash
# Increase swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Build Logs
```bash
# Verbose build output
buildozer android debug --verbose

# Check build logs
tail -f .buildozer/android/platform/build.log
```

## Testing APK

### Pre-Installation Testing
```bash
# Check APK file
file bin/tarotmac-debug.apk

# Verify APK signature
aapt dump badging bin/tarotmac-debug.apk

# Check APK size
ls -lh bin/tarotmac-debug.apk
```

### Installation Testing
```bash
# Install on connected device
adb install bin/tarotmac-debug.apk

# Check installation
adb shell pm list packages | grep tarotmac

# Launch app
adb shell am start -n com.tarotmac.android/.MainActivity
```

## Deployment

### Google Play Store
1. **Sign APK**: Use release keystore
2. **Upload**: Via Google Play Console
3. **Configure**: Store listing, screenshots, description
4. **Submit**: For review

### Direct Distribution
1. **Host APK**: On website or file sharing service
2. **Provide Instructions**: Installation guide
3. **Support**: User assistance for installation

## Build Artifacts

### Generated Files
- `bin/tarotmac-debug.apk` - Debug APK (~45MB)
- `bin/tarotmac-release.apk` - Release APK (~42MB)
- `.buildozer/` - Build cache and logs
- `build_artifacts/` - Additional build files

### File Locations
```
android/
├── bin/                          # Generated APK files
│   ├── tarotmac-debug.apk
│   └── tarotmac-release.apk
├── .buildozer/                   # Build cache
├── build_artifacts/              # Build documentation
├── buildozer.spec                 # Build configuration
└── BUILD_INSTRUCTIONS.md          # This file
```

## Performance Optimization

### APK Size Optimization
- Remove unused dependencies
- Optimize images and assets
- Enable ProGuard obfuscation
- Use APK splitting for different architectures

### Runtime Optimization
- Enable Python bytecode compilation
- Optimize Kivy/KivyMD imports
- Use lazy loading for heavy components
- Implement efficient memory management

## Security Considerations

### APK Signing
- Use strong keystore passwords
- Store keystore securely
- Backup keystore files
- Use different keystores for debug/release

### Code Protection
- Enable ProGuard obfuscation
- Remove debug information
- Validate input data
- Implement proper error handling

## Maintenance

### Regular Updates
- Update dependencies regularly
- Test on new Android versions
- Monitor performance metrics
- Address user feedback

### Build Environment
- Keep build tools updated
- Maintain clean build environment
- Document build process changes
- Version control build configurations

---

**Last Updated**: 2024-01-15  
**Version**: 1.0  
**Status**: Production Ready