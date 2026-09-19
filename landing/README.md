# GuruGraph landing page

A static page (no build step). It is live-ready once four placeholders are replaced.

## Before you deploy, replace

1. `YOUR_PROJECT_ID` (twice) and `gurugraph.vercel.app` (twice) with the values from your Raah project.
2. `https://forms.gle/REPLACE_WITH_PILOT_FORM` with your pilot sign-up form (Google Form or Tally).
3. `[[Team name]]` in the footer.
4. The GitHub button link, once your public repo exists.

## Raah (sponsor bonus points)

1. Sign up at https://raah.dev (the free tier is enough) and create a project for your domain.
2. Copy the project id into both snippets in `index.html`: the beacon in `<head>` and the badge in the footer.
3. In the Raah dashboard, turn on the public badge with mode "both" (live visitors and stats).
4. Optional: create a hosted status page for the API and link it from the deck.

## Deploy (pick one, about 5 minutes)

- **Vercel:** `npx vercel deploy --prod` from this folder, or import the repo in the Vercel dashboard with root directory `gurugraph/landing` and no build command.
- **Cloudflare Pages:** create a project, choose "Direct upload" and drag this folder in.

Then open the site on a phone, check the Raah dashboard shows the visit, and make the QR code for slide 5 point to it.
