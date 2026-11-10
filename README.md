# Cloudy AI Tool Finder

A free, static quiz + directory that matches people with the right AI tools for coding, vibe coding, AI agents, game dev, images, video, audio, writing, research and productivity.

- `data/tools.json` — curated tool dataset (sources in `data/sources.md`). Add `"affiliateUrl"` to a tool to use an affiliate link (rendered with `rel="sponsored"`).
- `src/` — CSS, JS (quiz + directory), favicon, OG image.
- `build.py` — generates the static site into `dist/` (home/quiz, directory, category pages, tool pages, sitemap.xml, robots.txt, llms.txt, llms-full.txt, JSON-LD).

```
BASE_URL=https://<user>.github.io/ai-tool-finder python3 build.py
```

Deployed to GitHub Pages from the `gh-pages` branch by `deploy.sh`. Built by Cloudy.
