#!/bin/bash

# Code signing script for macOS Tarot App
# Requires Apple Developer account and certificates

set -e

APP_NAME="Tarot"
APP_PATH="dist/${APP_NAME}.app"
IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
ENTITLEMENTS="entitlements.plist"

echo "🔐 Code signing ${APP_NAME}..."

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "❌ App not found at $APP_PATH"
    echo "Run 'python packaging/build_app.py' first"
    exit 1
fi

# Create entitlements file
cat > "$ENTITLEMENTS" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>
</dict>
</plist>
EOF

# Sign the app
echo "📝 Signing app bundle..."
codesign --force --verify --verbose --sign "$IDENTITY" --entitlements "$ENTITLEMENTS" "$APP_PATH"

# Verify the signature
echo "✅ Verifying signature..."
codesign --verify --verbose "$APP_PATH"
spctl --assess --verbose "$APP_PATH"

echo "🎉 Code signing complete!"
echo "App is ready for distribution at: $APP_PATH"