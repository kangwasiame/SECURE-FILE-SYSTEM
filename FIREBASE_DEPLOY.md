# Firebase deployment

This Flask app runs on Cloud Run, with Firebase Hosting providing the public HTTPS domain.

## Deploy

1. Install the Firebase CLI:

   ```powershell
   npm install -g firebase-tools
   firebase login
   ```

2. From this directory, select your Firebase project:

   ```powershell
   firebase use YOUR_FIREBASE_PROJECT_ID
   ```

3. Enable the required Google Cloud services:

   ```powershell
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
   ```

4. Build and deploy the container:

   ```powershell
   gcloud builds submit --tag gcr.io/YOUR_FIREBASE_PROJECT_ID/secure-file-system
   gcloud run deploy secure-file-system --image gcr.io/YOUR_FIREBASE_PROJECT_ID/secure-file-system --region us-central1 --allow-unauthenticated --set-env-vars SECRET_KEY=CHANGE_THIS_SECRET
   ```

5. Deploy Firebase Hosting:

   ```powershell
   firebase deploy --only hosting
   ```

`firebase.json` rewrites all public routes to the Cloud Run service.

## Storage note

The current app uses SQLite and local uploads. Cloud Run's local filesystem is ephemeral, so production deployment should move the database to Cloud SQL and file bytes to Cloud Storage before relying on uploaded files across restarts.
