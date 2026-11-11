#!/usr/bin/env python3
"""Static site generator for Cloudy AI Tool Finder. Usage: BASE_URL=https://x.github.io/repo python3 build.py"""
import json, os, shutil, html, datetime
from pathlib import Path
BASE = os.environ.get('BASE_URL', 'https://example.github.io/ai-tool-finder').rstrip('/')
SITE = 'Cloudy AI Tool Finder'
X_HANDLE = 'ItsCloudySpace'
NEWS = 'https://cloudys-newsletter.beehiiv.com/subscribe'
PROMPTS_SITE = 'https://itscloudy96.github.io/prompt-library/'
KITS_SITE = 'https://itscloudy96.github.io/game-dev-kits/'
TODAY = datetime.date.today().isoformat()
src, out = Path('src'), Path('dist')
D = json.load(open('data/tools.json'))
TOOLS, CATS = D['tools'], D['categories']
BY = {t['id']: t for t in TOOLS}
CAT_BLURB = {
 'code':'AI coding assistants, IDEs and CLI agents that help you write, refactor and ship software faster.',
 'vibe-code':'Vibe coding tools and AI app builders that turn a prompt into a working app or website.',
 'agents':'Frameworks, SDKs and no-code platforms for building AI agents and automating workflows.',
 'games':'AI tools for game development: prototyping, assets, engines, 3D models, music and voice.',
 'images':'AI image generators for art, concept design, logos, game assets and marketing visuals.',
 'video':'AI video generators and editors for shorts, trailers, avatars and devlogs.',
 'audio':'AI music, voice and audio tools for songs, voiceovers, podcasts and game sound.',
 'write':'AI chat assistants and writing tools for drafting, brainstorming and everyday questions.',
 'research':'AI research and answer engines that cite sources and help you learn faster.',
 'productivity':'AI productivity tools for meetings, notes, slides and automating busywork.'}
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def link(t): return t.get('affiliateUrl') or t['url']
def rel(t): return 'sponsored noopener' if t.get('affiliateUrl') else 'noopener'
def badge(t):
    c = {'free':'free','paid':'paid'}.get(t['pricingTier'],'')
    return f'<span class="badge {c}">{e(t["pricingTier"])}</span>'
def jl(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</','<\\/') + '</script>'
ORG = {"@type":"Organization","name":"Cloudy","url":BASE+'/',"sameAs":[f"https://x.com/{X_HANDLE}","https://cloudys-newsletter.beehiiv.com",PROMPTS_SITE,KITS_SITE]}

def page(path, title, desc, body, root, ld=None, ogtype='website'):
    url = BASE + '/' + path
    lds = ''.join(jl(x) for x in (ld or []))
    doc = f'''<!doctype html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b1020">
<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}"><meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@{X_HANDLE}">
<meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}/og.png">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" title="LLM summary" href="{root}llms.txt">
<link rel="stylesheet" href="{root}css/styles.css?v={TODAY}">
{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav">
<a class="logo" href="{root}"><span class="logo-mark" aria-hidden="true">☁️</span>Cloudy <span class="muted" style="font-weight:600">AI Tool Finder</span></a>
<nav class="nav-links" aria-label="Main"><a href="{root}#quiz-start">Quiz</a><a href="{root}tools/">All tools</a><a href="{PROMPTS_SITE}">Prompts</a><a href="{KITS_SITE}">Kits</a><a href="{root}about/">About</a><a href="{NEWS}" target="_blank" rel="noopener">Newsletter</a></nav>
</div></header>
<main id="main" class="container">
{body}
</main>
<footer class="footer"><div class="container footer-grid">
<div><strong>☁️ Cloudy</strong><p>Find the right AI tool in 30 seconds. Curated tools for builders, gamers and vibe coders.</p>
<form class="newsletter" action="{NEWS}" method="get" target="_blank"><input type="email" name="email" placeholder="you@example.com" aria-label="Email address" required><button class="btn btn-primary" type="submit">Get the daily AI agent brief</button></form></div>
<div><strong>Explore</strong><br>{'<br>'.join(f'<a href="{root}category/{k}/">{e(v)}</a>' for k,v in CATS.items())}</div>
<div><strong>Cloudy</strong><br><a href="{root}about/">About &amp; disclosure</a><br><a href="{root}about/#sponsor">Sponsor Cloudy</a><br><a href="{PROMPTS_SITE}">Prompt Library</a><br><a href="{KITS_SITE}">Game Dev Kits</a><br><a href="https://x.com/{X_HANDLE}" target="_blank" rel="noopener">@{X_HANDLE} on X</a><br><a href="{root}llms.txt">llms.txt</a><br><a href="{root}sitemap.xml">Sitemap</a></div>
</div><div class="container disclaimer" style="margin-top:1rem">© {datetime.date.today().year} Cloudy. Prices and features change often; confirm on each vendor's site. Data last reviewed {e(D['generatedAt'])}. Some outbound links may be affiliate links.</div></footer>
<script src="{root}js/app.js?v={TODAY}" defer></script>
</body></html>'''
    p = out / path
    if path == '' or path.endswith('/'): p = p / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(doc)

def card(t, root):
    cats = ''.join(f'<span class="badge">{e(c)}</span>' for c in t['categories'][:2])
    return (f'<article class="card tool-card"><h3><a href="{root}tool/{t["id"]}/">{e(t["name"])}</a></h3><div>{badge(t)}{cats}</div>'
            f'<p>{e(t["bestFor"])}</p><div class="meta"><a href="{root}tool/{t["id"]}/">Details →</a>'
            f'<a href="{e(link(t))}" target="_blank" rel="{rel(t)}">Visit ↗</a></div></article>')
SPONSOR = lambda root: (f'<aside class="card sponsor" aria-label="Sponsor"><div class="label">Sponsor slot</div><h3 style="margin:.3rem 0">Your AI tool here</h3>'
    f'<p class="muted" style="margin:0 0 .6rem">Reach builders, gamers and vibe coders actively choosing AI tools.</p><a class="btn btn-secondary btn-sm" href="{root}about/#sponsor">Sponsor this spot</a></aside>')
def in_cat(c): return [t for t in TOOLS if c in t['categories']]

def build():
    if out.exists(): shutil.rmtree(out)
    shutil.copytree(src, out)
    (out/'data').mkdir(exist_ok=True)
    shutil.copy('data/tools.json', out/'data/tools.json')
    (out/'.nojekyll').write_text('')
    urls = []
    # ---- home
    faqs = [("What is the Cloudy AI Tool Finder?", f"A free 6-question quiz and directory that matches you with AI tools for coding, vibe coding, AI agents, game development, images, video, audio, writing, research and productivity. It covers {len(TOOLS)} hand-picked tools."),
            ("How are tools ranked?", "Each tool is scored on how well it fits your goal, skill level, budget, preferred workspace and priorities. Sponsorships and affiliate links never change the ranking."),
            ("What is the best free AI coding tool?", "Good free starting points are GitHub Copilot Free, Aider (open source, bring your own model), Continue (open source) and the free tiers of Cursor and Devin Desktop (formerly Windsurf)."),
            ("What is the best AI tool for vibe coding?", "For no-setup browser building, try Lovable, Bolt, v0 or Replit. For bigger projects, Cursor, Claude Code and Codex give you more control."),
            ("Are the prices accurate?", f"Prices were checked against vendor pages and recent reviews (last reviewed {D['generatedAt']}). AI pricing changes often, so always confirm on the vendor site.")]
    cats_html = ''.join(f'<a class="card" href="category/{k}/"><strong>{e(v)}</strong><div class="count">{len(in_cat(k))} tools</div></a>' for k,v in CATS.items())
    feat = [BY[i] for i in ['cursor','claude-code','lovable','n8n','rosebud','elevenlabs'] if i in BY]
    body = f'''
<section class="hero" id="quiz-start">
<div class="pill-row"><span class="pill">🤖 AI agents</span><span class="pill">⚡ Vibe coding</span><span class="pill">🎮 Game dev</span><span class="pill">🎨 Creative AI</span></div>
<h1>Find your perfect AI tool<br>in 30 seconds.</h1>
<p>Answer 6 quick questions and get a ranked shortlist from {len(TOOLS)} curated AI tools, with real pricing, strengths and trade-offs. Free, no sign-up.</p>
</section>
<section class="card quiz-card" id="quiz" aria-live="polite"><noscript>The quiz needs JavaScript. You can still <a href="tools/">browse all tools</a>.</noscript></section>
<section class="section"><h2>Browse by category</h2><div class="cat-grid">{cats_html}</div></section>
<section class="section"><h2>Popular picks</h2><div class="grid">{''.join(card(t,'') for t in feat)}{SPONSOR('')}</div></section>
<section class="section card"><h2>Get the daily AI agent brief</h2><p class="muted">New agent tools, model updates and vibe-coding tricks in a 3-minute read. Free.</p>
<form class="newsletter" action="{NEWS}" method="get" target="_blank"><input type="email" name="email" placeholder="you@example.com" aria-label="Email address" required><button class="btn btn-primary" type="submit">Subscribe free</button></form></section>
<section class="section"><h2>Also from Cloudy</h2><div class="grid"><a class="card" href="{PROMPTS_SITE}" style="color:var(--text);text-decoration:none"><strong>☁️ Prompt Library</strong><p class="muted" style="margin:.4rem 0 0">64 original, copy-ready prompts and agent configs for Cursor, Claude, ChatGPT and more.</p></a>
<a class="card" href="{KITS_SITE}" style="color:var(--text);text-decoration:none"><strong>☁️ Game Dev Kits</strong><p class="muted" style="margin:.4rem 0 0">Free, playable starter games with a downloadable zip and a vibe-coding prompt pack.</p></a>
<a class="card" href="{NEWS}" target="_blank" rel="noopener" style="color:var(--text);text-decoration:none"><strong>✉️ Cloudy newsletter</strong><p class="muted" style="margin:.4rem 0 0">The daily AI agent changelog, in a 3-minute read. Free.</p></a></div></section>
<section class="section faq"><h2>FAQ</h2>{''.join(f'<details><summary>{e(q)}</summary><p class="muted">{e(a)}</p></details>' for q,a in faqs)}</section>'''
    ld = [{"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":BASE+'/',"description":"Quiz and directory that matches you with the right AI tools.","publisher":ORG,
           "potentialAction":{"@type":"SearchAction","target":BASE+"/tools/?q={search_term_string}","query-input":"required name=search_term_string"}},
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
          {"@context":"https://schema.org", **ORG}]
    page('', f'{SITE}: Find the Best AI Tool for You (Quiz)', f'Take a 30-second quiz to find the best AI tools for coding, vibe coding, AI agents, game dev, images, video and more. {len(TOOLS)} curated tools with real pricing.', body, '', ld); urls.append(('', '1.0'))
    # ---- directory
    opts = ''.join(f'<option value="{k}">{e(v)}</option>' for k,v in CATS.items())
    body = f'''<p class="crumbs"><a href="../">Home</a> / All tools</p>
<section class="hero" style="padding-top:1.5rem"><h1>All AI tools</h1><p>Search and filter {len(TOOLS)} curated AI tools by category, price and skill level.</p></section>
<div class="filters"><input id="f-q" type="search" placeholder="Search tools, e.g. “agent”, “3d”, “music”" aria-label="Search">
<select id="f-cat" aria-label="Category"><option value="">All categories</option>{opts}</select>
<select id="f-price" aria-label="Pricing"><option value="">Any price</option><option value="free-tier">Has a free tier</option><option value="free">Free / open source</option><option value="freemium">Freemium</option><option value="paid">Paid</option></select>
<select id="f-skill" aria-label="Skill level"><option value="">Any skill</option><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></div>
<p class="muted" id="dir-count">{len(TOOLS)} tools</p>
<div class="grid" id="dir-grid">{''.join(card(t,'../') for t in TOOLS)}</div>
<div class="section">{SPONSOR('../')}</div>'''
    ld = [{"@context":"https://schema.org","@type":"ItemList","name":"AI tools directory","numberOfItems":len(TOOLS),
           "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/tool/{t['id']}/","name":t['name']} for i,t in enumerate(TOOLS)]}]
    page('tools/', f'AI Tools Directory ({len(TOOLS)} tools, 2026) | Cloudy', f'Browse {len(TOOLS)} AI tools for coding, agents, game dev, images, video, audio, writing and productivity. Filter by price and skill level.', body, '../', ld); urls.append(('tools/','0.9'))
    # ---- categories index
    body = f'<p class="crumbs"><a href="../">Home</a> / Categories</p><section class="hero" style="padding-top:1.5rem"><h1>AI tool categories</h1><p>Pick a lane. Every list is curated with real pricing and trade-offs.</p></section><div class="cat-grid">' + \
        ''.join(f'<a class="card" href="{k}/"><strong>{e(v)}</strong><div class="count">{len(in_cat(k))} tools</div><p class="muted" style="font-size:.85rem;margin:.4rem 0 0">{e(CAT_BLURB[k])}</p></a>' for k,v in CATS.items()) + '</div>'
    page('category/', 'AI Tool Categories | Cloudy AI Tool Finder', 'Browse AI tools by category: coding, vibe coding, AI agents, game development, images, video, audio, writing, research and productivity.', body, '../'); urls.append(('category/','0.8'))
    for k, v in CATS.items():
        lst = in_cat(k)
        lst.sort(key=lambda t: (t['categories'].index(k), t['name'].lower()))
        rows = ''.join(f'<tr><td><a href="../../tool/{t["id"]}/">{e(t["name"])}</a></td><td>{e(t["pricing"])}</td><td>{e(", ".join(t["skillLevels"]))}</td></tr>' for t in lst)
        body = f'''<p class="crumbs"><a href="../../">Home</a> / <a href="../">Categories</a> / {e(v)}</p>
<section class="hero" style="padding-top:1.5rem"><h1>Best AI tools for {e(v.lower())} (2026)</h1><p>{e(CAT_BLURB[k])} {len(lst)} picks, compared.</p>
<div><a class="btn btn-primary" href="../../#quiz-start">Not sure? Take the 30-second quiz</a></div></section>
<div class="grid">{''.join(card(t,'../../') for t in lst)}{SPONSOR('../../')}</div>
<section class="section"><h2>Quick pricing comparison</h2><div class="card" style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:.9rem">
<thead><tr><th align="left">Tool</th><th align="left">Pricing</th><th align="left">Skill level</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="disclaimer">Pricing last reviewed {e(D['generatedAt'])}. Confirm on each vendor's site.</p></section>'''
        ld = [{"@context":"https://schema.org","@type":"ItemList","name":f"Best AI tools for {v}","numberOfItems":len(lst),
               "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/tool/{t['id']}/","name":t['name']} for i,t in enumerate(lst)]},
              {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+'/'},{"@type":"ListItem","position":2,"name":"Categories","item":BASE+'/category/'},{"@type":"ListItem","position":3,"name":v,"item":f"{BASE}/category/{k}/"}]}]
        page(f'category/{k}/', f'Best AI Tools for {v} (2026) | Cloudy', f'{CAT_BLURB[k]} Compare {len(lst)} tools by price, skill level, strengths and weaknesses.', body, '../../', ld); urls.append((f'category/{k}/','0.8'))
    # ---- tool pages
    for t in TOOLS:
        prim = t['categories'][0]
        alts = [x for x in TOOLS if x['id'] != t['id'] and prim in x['categories']][:4]
        catlinks = ' '.join(f'<a class="badge" href="../../category/{c}/">{e(CATS.get(c,c))}</a>' for c in t['categories'])
        body = f'''<p class="crumbs"><a href="../../">Home</a> / <a href="../../category/{prim}/">{e(CATS[prim])}</a> / {e(t["name"])}</p>
<section class="hero" style="padding-top:1.5rem"><h1>{e(t["name"])}</h1><p>{e(t["bestFor"])}.</p><div>{badge(t)}{'<span class="badge free">free tier</span>' if t['freeTier'] else ''} {catlinks}</div>
<div><a class="btn btn-primary" href="{e(link(t))}" target="_blank" rel="{rel(t)}">Visit {e(t["name"])} ↗</a></div></section>
<section class="card"><div class="kv"><div><strong>Pricing</strong><span>{e(t["pricing"])}</span></div><div><strong>Best for</strong><span>{e(t["bestFor"])}</span></div>
<div><strong>Skill level</strong><span>{e(", ".join(t["skillLevels"]))}</span></div><div><strong>Tags</strong><span>{e(", ".join(t["tags"]))}</span></div>
<div><strong>Website</strong><span><a href="{e(t["url"])}" target="_blank" rel="noopener">{e(t["url"])}</a></span></div></div></section>
<section class="section compare"><div class="card"><h2>Strengths</h2><ul class="list-good">{''.join(f'<li>{e(s)}</li>' for s in t["strengths"])}</ul></div>
<div class="card"><h2>Watch out for</h2><ul class="list-bad">{''.join(f'<li>{e(s)}</li>' for s in t["weaknesses"])}</ul></div></section>
<section class="section"><h2>Alternatives to {e(t["name"])}</h2><div class="grid">{''.join(card(a,'../../') for a in alts)}</div></section>
<section class="section card"><h2>Is {e(t["name"])} right for you?</h2><p class="muted">Take the 30-second quiz to see how it ranks against {len(TOOLS)-1} other tools for your goal and budget.</p><a class="btn btn-primary" href="../../#quiz-start">Take the quiz</a></section>
<p class="disclaimer">Last reviewed {e(D['generatedAt'])}. Prices and features change; confirm on the vendor's site.</p>'''
        ld = [{"@context":"https://schema.org","@type":"SoftwareApplication","name":t['name'],"url":t['url'],"applicationCategory":"BusinessApplication" if prim in ('productivity','agents') else ("GameApplication" if prim=='games' else "DeveloperApplication" if prim in ('code','vibe-code') else "MultimediaApplication"),
               "operatingSystem":"Web, Windows, macOS, Linux","description":t['bestFor'],"keywords":", ".join(t['tags']),
               "isAccessibleForFree":bool(t['freeTier'])},
              {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+'/'},{"@type":"ListItem","position":2,"name":CATS[prim],"item":f"{BASE}/category/{prim}/"},{"@type":"ListItem","position":3,"name":t['name'],"item":f"{BASE}/tool/{t['id']}/"}]}]
        page(f'tool/{t["id"]}/', f'{t["name"]} Review: Pricing, Pros & Cons, Alternatives (2026) | Cloudy', f'{t["name"]}: {t["bestFor"]}. Pricing: {t["pricing"]}'[:300], body, '../../', ld, 'article'); urls.append((f'tool/{t["id"]}/','0.7'))
    # ---- about
    body = f'''<p class="crumbs"><a href="../">Home</a> / About</p><section class="section prose"><h1>About Cloudy</h1>
<p>Cloudy builds free, fast tools for people into AI, AI agents, vibe coding, tech and video games. The AI Tool Finder matches you with the right tools in 30 seconds, from a hand-curated list of {len(TOOLS)} real products.</p>
<p>Need a prompt instead of a product? The <a href="{PROMPTS_SITE}">Cloudy Prompt Library</a> has original, copy-ready system prompts, Cursor rules, agent templates and more.</p>
<p>Want to make a game? <a href="{KITS_SITE}">Cloudy Game Dev Kits</a> are free, MIT-licensed starters with a playable demo and a prompt pack.</p>
<h2>How we pick and rank tools</h2><ul><li>Only real, publicly available tools, with pricing checked against vendor pages and recent reviews.</li><li>The quiz scores fit: goal, skill level, budget, workspace and priorities.</li><li>Money never buys a ranking. Sponsored placements are always labeled.</li></ul>
<h2>Affiliate disclosure</h2><p>Some outbound links may be affiliate links, which means Cloudy may earn a commission at no extra cost to you. Affiliate links are marked with <code>rel="sponsored"</code> and never affect quiz results.</p>
<h2 id="sponsor">Sponsor Cloudy</h2><p>Want your AI tool in front of builders and vibe coders? Sponsor slots are available on the site and in the Cloudy newsletter. Send a DM to <a href="https://x.com/{X_HANDLE}" target="_blank" rel="noopener">@{X_HANDLE}</a> on X.</p>
<h2>Corrections</h2><p>Spotted outdated pricing or a missing tool? DM <a href="https://x.com/{X_HANDLE}" target="_blank" rel="noopener">@{X_HANDLE}</a> and we'll fix it.</p>
<h2>Newsletter</h2><p><a href="{NEWS}" target="_blank" rel="noopener">Subscribe to the Cloudy newsletter</a> for a daily AI agent brief.</p></section>'''
    page('about/', 'About Cloudy & Disclosure | Cloudy AI Tool Finder', 'How Cloudy picks and ranks AI tools, affiliate disclosure and sponsorship info.', body, '../'); urls.append(('about/','0.4'))
    # ---- 404
    from urllib.parse import urlparse
    pre = urlparse(BASE).path.rstrip('/') + '/'
    page('404.html', 'Page not found | Cloudy AI Tool Finder', 'This page does not exist.', f'<section class="hero"><h1>Lost in the clouds ☁️</h1><p>That page doesn\'t exist. Try the quiz or browse all tools.</p><div><a class="btn btn-primary" href="{pre}">Take the quiz</a> <a class="btn btn-secondary" href="{pre}tools/">All tools</a></div></section>', pre)
    # ---- sitemap / robots / llms
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for u,p in urls) + '</urlset>\n'
    (out/'sitemap.xml').write_text(sm)
    (out/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\n# AI crawlers welcome\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    L = [f'# {SITE}', '', f'> Free quiz and directory that matches people with the right AI tools. {len(TOOLS)} curated, real tools across {len(CATS)} categories, with pricing last reviewed {D["generatedAt"]}. Run by Cloudy.', '',
         'Data is available as JSON at ' + BASE + '/data/tools.json (fields: name, url, categories, pricing, pricingTier, freeTier, skillLevels, strengths, weaknesses, bestFor, tags).', '', '## Main pages',
         f'- [Quiz]({BASE}/): 6-question AI tool recommender', f'- [All tools]({BASE}/tools/): searchable directory', f'- [Full tool list for LLMs]({BASE}/llms-full.txt)', f'- [About & disclosure]({BASE}/about/)', '', '## Categories']
    L += [f'- [{v}]({BASE}/category/{k}/): {CAT_BLURB[k]}' for k,v in CATS.items()]
    L += ['', '## Tools'] + [f'- [{t["name"]}]({BASE}/tool/{t["id"]}/): {t["bestFor"]}. Pricing: {t["pricing"]}' for t in TOOLS]
    (out/'llms.txt').write_text('\n'.join(L)+'\n')
    F = [f'# {SITE}: full tool data', f'Last reviewed {D["generatedAt"]}. {D["disclaimer"]}', '']
    for k,v in CATS.items():
        F += [f'## {v}', CAT_BLURB[k], '']
        for t in in_cat(k):
            F += [f'### {t["name"]}', f'- Website: {t["url"]}', f'- Page: {BASE}/tool/{t["id"]}/', f'- Pricing: {t["pricing"]} (tier: {t["pricingTier"]}, free tier: {"yes" if t["freeTier"] else "no"})',
                  f'- Best for: {t["bestFor"]}', f'- Skill levels: {", ".join(t["skillLevels"])}', f'- Strengths: {"; ".join(t["strengths"])}', f'- Weaknesses: {"; ".join(t["weaknesses"])}', '']
    (out/'llms-full.txt').write_text('\n'.join(F))
    print('built', len(urls), 'pages ->', out, 'BASE', BASE)
if __name__ == '__main__': build()
