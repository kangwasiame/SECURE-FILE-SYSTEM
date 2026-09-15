# Permanent public access

The Cloudflare quick tunnel is temporary. For permanent access, deploy this repository as the Render web service described in `render.yaml`.

## Render

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint** and select this repository.
3. Render reads `render.yaml`, creates the service, and provides a stable HTTPS hostname.
4. Keep the generated `SECRET_KEY` and attach the persistent disk so the database and uploads survive restarts.

The default hostname is expected to be:

`https://vault-secure-file-storage.onrender.com`

## Custom permanent address

A website cannot guarantee a permanent public IP from application code. Public IPs belong to the hosting provider and can change. For a memorable permanent address, add a domain in Render and point its DNS records to Render. The domain remains stable even if the provider changes the underlying IP.

For a fixed numeric IP, use a hosting provider that explicitly offers a dedicated/static IP and configure DNS and HTTPS there.
