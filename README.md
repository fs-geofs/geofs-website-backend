# Geofs-Website-Backend

_"A poor man's content management system" - JPH_

Backend to deliver info from easily adaptable JSON files via an API tp the website
frontend.

This backend is meant to be used in combination with the following repositories:

- Frontend: 
  [fs-geofs/geofs-website](https://github.com/fs-geofs/geofs-website)
- Content:
  [fs-geofs/geofs-website-content](https://github.com/fs-geofs/geofs-website-content)

## Installation

Python 3.12 was used while developing this backend, it is recommended to use a virtual
environment for developments.

- Install dependencies using `pip install -r requirements.txt`
- (optional:) set ENVs if you want to use Github Mode (see below)
- To start the server in dev mode, run `run.py`

## Backend Modes

This backend supports two modes for editing content.

### File mode

To make changes to data which this backend serves, one simply edits the JSON files and
saves them. Files are located in `./data`

### Github mode

For more convenient editing, files are editied inside the Github content repository.
When changes are pushed on the `main` branch, a webhook in github triggers the backend 
to pull the content repository to get the latest updates. Files are located in 
`../git-content/<content-repo-name>`

In this case, files **must not** be edited through the file system so they do not fall
out of sync with the content repository on Github. They **must** be edited on Github.

Another advantage is that using this mode we get versioning and some sort of backups
on top for free.

## Webhooks
 
The following are instructions to set up the webhook on Github to auto-update.
To enable this functionality, both ENVs (see below) must be set when running the backend

### For Prod

1. Go to [Content Repo](https://github.com/fs-geofs/geofs-website-content)
2. Settings -> Webhooks -> Add Webhook
3. Fill the following:
   - URL: `https://<public-domain>/webhook/update-website-content/`
   - Content-Type: `application/json`
   - Secret: A very secret text string, remember for later
   - Just the `push` event 
4. Click Activate webhook
5. In the reverse proxy, make the following rules, here example for nginx.
6. Note that github might change in the future, most recent ones are listed 
   [here](https://api.github.com/meta) under `hooks`.
   ```
   # expose webhook to update website content, proxy to webhook endpoint
   location /webhook/update-website-content/ {
   	    
       # allow github IPs
       allow 192.30.252.0/22;
       allow 185.199.108.0/22;
       allow 140.82.112.0/20;
       allow 143.55.64.0/20;
       allow 2a0a:a440::/29;
       allow 2606:50c0::/32;
   
       # disallow all others
       deny all;
       
       proxy_pass http://website-backend:8000/webhook/update-website-content;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   	
   # disallow calls to any sub-paths
   location ^~ /webhook/update-website-content/* {
       return 404;
   }
   ```
   
### For Dev

For development, use webhook-forwarding to forward the Github's webook request to the 
local environment.

1. Install [Github-CLI](https://cli.github.com/)
2. Run the following command, replace <secret-from-above> with the secret text string
   that was used while setting up the webhook.
   ```shell
   gh webhook forward \
     --repo=fs-geofs/geofs-website-content \
     --events=push \
     --url=http://localhost/webhook/update-website-content/ \
     --secret <secret-from-above>
   ```

## ENVs

For running this backend in Github mode, both the following ENVs must be set:

- GITHUB_WEBHOOK_SECRET: _secret text that was already set above_
- GITHUB_CONTENT_REPO: Name of the repository that holds the content
  i.e. `fs-geofs/geofs-website-content`

If none of the ENVs is set, the backend will use file editing mode, no github 
integration is available and the webhook will not work.

If one of the two ENVs is set, the Server will not start.
