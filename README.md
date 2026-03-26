# Endless Clickomania
So far, my best is 58.

Play it at **https://clickomania.pages.dev/**

By [Alexei 'keyhell' Zhurba](https://keyhell.org/)

## Bomb Cells
Occasionally a black cell appears when the board refills. Clicking a bomb now clears a small 3×3 area around it rather than an entire row and column, making them a little less powerful.

## Offline Play

Clickomania is now a Progressive Web App. The core HTML, JavaScript, and assets are cached with a service worker so the game continues to load even when the device is offline or in airplane mode. Every time the page is opened, a fresh board is generated and the score counters reset, mirroring the behaviour of a manual restart.

## Automatic Version Bumps

Each commit must bump the PWA build number so browsers pick up the latest cache. This repository ships with a pre-commit hook that runs `scripts/bump_version.py`, which increments the build counter and propagates the new version to `manifest.json`, `service-worker.js`, and the `app-version` meta tag in `index.html`.

To activate the hook, point Git at the bundled hooks directory (run once per clone):

```
git config core.hooksPath .githooks
```

After that, each commit automatically updates the version metadata and stages the modified files for you.
