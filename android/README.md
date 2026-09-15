# Vault Android app

This is a WebView wrapper for the Flask application.

## Build for the local Flask server

1. Start Flask from the repository root: `python run.py`
2. Start an Android emulator.
3. Build the debug APK:

```powershell
./gradlew assembleDebug
```

The APK will be at `app/build/outputs/apk/debug/app-debug.apk`.

## Build for a deployed server

Pass the public HTTPS URL when building:

```powershell
./gradlew assembleRelease -PserverUrl=https://your-domain.example/
```

The default URL `http://10.0.2.2:5000/` is for an Android emulator reaching Flask on the host computer. A physical phone needs a reachable HTTPS URL or a LAN address configured with `-PserverUrl`.
