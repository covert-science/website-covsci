# Deploying the website on Cloudflare

The site is static HTML, CSS and images. The only external calls are Google
Fonts and the contact form, which posts to formsubmit.co. Nothing depends on a
VPS backend, so it is served directly from Cloudflare Workers static assets
(`wrangler.jsonc`). This replaces the file server on the Hetzner VPS
(`/opt/asc-qdrant/covsci`, Caddy vhost `covert.science`).

## First deployment

1. Sign in to the Cloudflare account that holds the `covert.science` and
   `covert-science.com` zones (their nameservers are rex/treasure; the
   `voodooflex.com` zone is on a different account).
2. In that account's DNS, delete the `A` records for `covert.science`,
   `www.covert.science`, `covert-science.com` and `www.covert-science.com`
   that point at 167.233.62.84. Custom domains cannot be attached while a
   conflicting record exists.
3. From a checkout of this repository:

   ```sh
   npx wrangler login
   npx wrangler deploy
   ```

   `routes` in `wrangler.jsonc` attach the four hostnames as custom domains and
   create their DNS records. `_redirects` sends the three aliases to
   `https://covert.science`, as the Hetzner Caddy did. `_headers` adds basic
   security headers. `.assetsignore` keeps tooling out of the published assets.

4. Verify: `curl -I https://covert.science/` returns 200, the aliases return
   301 to covert.science, images load, and the contact form still posts.

`voodooflex.com` and `www.voodooflex.com` also redirected to covert.science from
Hetzner. They are in the other Cloudflare account, so configure a Redirect Rule
there (or leave their A records on Hetzner until that host is retired).

## Updating

Commit, then `npx wrangler deploy` again. Each deploy is a new version; the
Workers dashboard allows rollback to a previous version.

## Removing the Hetzner copy

Only after the four hostnames resolve to Cloudflare and have been verified:
remove the `covert.science` block and the alias redirect block from
`/opt/asc-qdrant/Caddyfile`, reload Caddy with `caddy-reload.sh`, and archive
`/opt/asc-qdrant/covsci`. The static files are identical to this repository's
`master` (checked 2026-10-19).
