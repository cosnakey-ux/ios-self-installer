# iOS Self-Installer

A beautiful web interface to download and install iOS apps directly on your device without the App Store.

## Quick Start

### Option 1: GitHub Pages (Online)
Your app is already hosted at:
👉 **https://cosnakey-ux.github.io/ios-self-installer/**

Just visit from your iPad and download!

### Option 2: Local Server
Run locally with Python:

```bash
python3 server.py
```

Then open: `http://localhost:8000` (or your network IP)

## Setup Instructions

### Enable GitHub Pages
1. Go to your repository settings
2. Scroll to "GitHub Pages" section
3. Set Source to: `Deploy from a branch`
4. Select branch: `main`
5. Select folder: `/ (root)`
6. Click Save

Your site will be live at: `https://cosnakey-ux.github.io/ios-self-installer/`

### Add Your IPA File

#### For Local Server:
1. Build your iOS app in Xcode
2. Generate the IPA file
3. Place `SelfInstaller.ipa` in the repo root directory
4. Run `python3 server.py`

#### For GitHub Pages:
1. Go to your repo
2. Create a "Releases" on GitHub
3. Upload your `.ipa` file as a release asset
4. Update the download links in `index.html` to point to the release

## Features

✅ One-tap installation on iPad  
✅ No App Store required  
✅ Beautiful, responsive UI  
✅ Download progress tracking  
✅ Enterprise manifest support  
✅ File browser  
✅ Server status API  

## Files

- `index.html` - Beautiful web interface
- `server.py` - Python HTTP server (for local testing)
- `README.md` - This file

## iPad Installation Steps

1. Open Safari on your iPad
2. Visit the URL (local or GitHub Pages)
3. Click "📥 Download IPA"
4. Open Files app
5. Go to Downloads
6. Tap the .ipa file
7. Confirm installation

## Troubleshooting

**"Untrusted Developer" Warning?**
- Go to Settings → General → VPN & Device Management
- Find your app under "Enterprise App"
- Tap "Trust" to proceed

**Can't download from GitHub Pages?**
- GitHub Pages has size limits
- For large IPAs, use the local Python server instead
- Or host on a different service

**Need a real provisioning profile?**
- This requires an Apple Developer account
- Sign your app with your certificate
- Use xcode-select or fastlane to automate builds

## Architecture

The installer works by:
1. Serving an `.ipa` file over HTTP
2. Allowing iOS to download and install it
3. The app can then update itself by checking for newer versions

## Security Note

⚠️ Only download and install apps from trusted sources!

This implementation is for testing and development. Production apps should be properly signed and distributed through official channels.

## License

MIT - Feel free to use and modify!
