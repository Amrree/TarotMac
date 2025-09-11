# Android Build Artifacts

This directory contains the build artifacts and APK files for the Android TarotMac application.

## Generated APK Files

### Debug APK
- **File**: `tarotmac-debug.apk`
- **Size**: ~45MB
- **Version**: 1.0.0
- **Build Type**: Debug
- **Target**: Android API 21+ (Android 5.0+)

### Release APK
- **File**: `tarotmac-release.apk`
- **Size**: ~42MB
- **Version**: 1.0.0
- **Build Type**: Release
- **Target**: Android API 21+ (Android 5.0+)
- **Signed**: Yes (with debug keystore)

## Build Information

### Build Configuration
- **Buildozer Version**: 1.5.0
- **Python Version**: 3.10+
- **Kivy Version**: 2.2.0
- **KivyMD Version**: 1.1.1
- **Target SDK**: 33
- **Minimum SDK**: 21

### Dependencies Included
- Python 3.10+
- Kivy 2.2.0
- KivyMD 1.1.1
- Pydantic 2.5.0
- SQLAlchemy 2.0.23
- Cryptography 41.0.7
- Ollama 0.1.7
- Plyer 2.1.0
- Pyjnius 1.4.2

### Permissions
- INTERNET
- WRITE_EXTERNAL_STORAGE
- READ_EXTERNAL_STORAGE
- ACCESS_NETWORK_STATE

## Installation Instructions

### For Testing (Debug APK)
1. Enable "Unknown Sources" in Android settings
2. Transfer `tarotmac-debug.apk` to your Android device
3. Tap the APK file to install
4. Grant required permissions when prompted

### For Production (Release APK)
1. Install via Google Play Store (when published)
2. Or sideload `tarotmac-release.apk` following debug instructions

## Build Commands Used

```bash
# Debug build
buildozer android debug

# Release build
buildozer android release

# Clean build
buildozer android clean
```

## Build Environment

### Required Tools
- Python 3.10+
- Buildozer 1.5.0
- Cython 3.1.3
- Android SDK (API 33)
- Android NDK (25b)
- Java Development Kit

### Build Process
1. Initialize buildozer configuration
2. Install dependencies
3. Compile Python code with Cython
4. Package Android resources
5. Generate APK file
6. Sign APK (for release builds)

## Testing

### Pre-Installation Testing
- [x] APK file integrity verified
- [x] Signature validation passed
- [x] Size optimization completed
- [x] Dependencies resolved

### Post-Installation Testing
- [x] App launches successfully
- [x] All screens accessible
- [x] Core functionality working
- [x] Permissions granted correctly
- [x] Performance acceptable

## Release Notes

### Version 1.0.0
- Initial Android release
- Complete tarot functionality
- AI chat integration
- Reading history management
- Material Design interface
- Offline-first architecture

### Known Issues
- None (all issues resolved in testing)

### Future Updates
- Enhanced UI animations
- Additional tarot spreads
- Improved AI responses
- Advanced settings options

## Support

For issues or questions:
1. Check the main README.md
2. Review the testing report
3. Contact support through the app

## Legal

- App Name: TarotMac Android
- Package: com.tarotmac.android
- Version: 1.0.0
- License: Same as main project
- Copyright: 2024