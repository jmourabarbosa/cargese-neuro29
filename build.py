#!/usr/bin/env python3
"""Generate the static pages of the conference website.

Edit the data below (speakers, organizers, texts) and run:  python3 build.py
Photos: put a square JPEG at img/people/<slug>.jpg (slug = lowercase name with
hyphens, e.g. alex-williams.jpg). Missing photos fall back to initials.
"""
import html
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))

TITLE = "Cargèse 2029"
SUBTITLE = "Theoretical Neuroscience: Dynamics, Geometry and Learning"
DATES = "Dates to be announced"
VENUE = "Institut d'Études Scientifiques de Cargèse, Corsica"

# Confirmed speakers only: (name, institution, theme)
SPEAKERS = [
    ("Alex Williams", "New York University", "Geometry"),
    ("Alex Cayco-Gajic", "École Normale Supérieure, Paris", "Geometry"),
    ("Valeria Fascianelli", "Columbia University", "Geometry"),
    ("Ramon Nogueira", "University of Chicago", "Geometry"),
    ("Pedro Gonçalves", "KU Leuven", "Statistical models"),
    ("Joana Soldado Magraner", "Carnegie Mellon University", "Statistical models"),
    ("Jonathan Pillow", "Princeton University", "Statistical models"),
    ("Zachary Kilpatrick", "University of Colorado Boulder", "Neural circuits"),
    ("Francesca Mastrogiuseppe", "SISSA, Trieste", "Neural circuits"),
    ("Leenoy Meshulam", "Brown University", "Neural circuits"),
    ("Yonathan Aljadeff", "UC San Diego", "Neural circuits"),
    ("Andrew Saxe", "Gatsby Unit, University College London", "Learning"),
    ("Francesca Mignacco", "Princeton University", "Learning"),
    ("Sebastian Goldt", "SISSA, Trieste", "Learning"),
    ("Samuel Muscinelli", "University of Chicago", "Learning"),
    ("Dan Levenstein", "Yale University", "NeuroAI"),
    ("Ulises Pereira", "Allen Institute", "NeuroAI"),
    ("Richard Gao", "Goethe University Frankfurt", "NeuroAI"),
]

ORGANIZERS = [
    ("Joao Barbosa", "Neuromodulation Institute, INSERM, France"),
    ("Lea Duncker", "Columbia University, USA"),
    ("Lorenzo Fontolan", "INMED, INSERM, France"),
    ("Agostina Palmigiano", "Gatsby Computational Neuroscience Unit, UCL, UK"),
    ("Lorenzo Posani", "Paris Brain Institute, CNRS, France"),
]

SCIENTIFIC_COMMITTEE = [
    ("Srdjan Ostojic", "CNRS, École Normale Supérieure, Paris"),
    ("Aleksandra Walczak", "CNRS, École Normale Supérieure, Paris"),
    ("Claudia Clopath", "Imperial College London"),
]

# Homepage linked from each person's photo and name
URLS = {
    "Alex Williams": "https://alexhwilliams.info/",
    "Alex Cayco-Gajic": "https://caycogajiclab.github.io/",
    "Ramon Nogueira": "https://datascience.uchicago.edu/people/ramon-nogueira/",
    "Pedro Gonçalves": "https://ppjgoncalves.github.io/",
    "Joana Soldado Magraner": "https://jsoldadomagraner.github.io/",
    "Zachary Kilpatrick": "https://www.colorado.edu/neuroscience/zachary-kilpatrick",
    "Leenoy Meshulam": "https://physics.brown.edu/people/leenoy-meshulam",
    "Yonathan Aljadeff": "https://aljadeff.ucsd.edu/",
    "Andrew Saxe": "https://www.saxelab.org/",
    "Dan Levenstein": "https://medicine.yale.edu/profile/daniel-levenstein/",
    "Richard Gao": "https://rdgao.github.io/",
    "Joao Barbosa": "https://jbarbosa.org/",
    "Lea Duncker": "https://leaduncker.github.io/",
    "Lorenzo Fontolan": "https://fontolanl.github.io/",
    "Agostina Palmigiano": "https://palmigianolab.com/",
    "Lorenzo Posani": "https://lorenzoposani.com/",
    "Valeria Fascianelli": "https://valeriafascianelli.com/",
    "Francesca Mastrogiuseppe": "https://iris.sissa.it/cris/rp/rp26328",
    "Francesca Mignacco": "https://www.simonsfoundation.org/people/francesca-mignacco/",
    "Sebastian Goldt": "https://datascience.sissa.it/research-unit/12/theory-of-neural-networks",
    "Samuel Muscinelli": "https://cns.uchicago.edu/faculty/samuel-muscinelli",
    "Ulises Pereira": "https://ulisespereira.github.io/",
    "Srdjan Ostojic": "https://lnc2.dec.ens.fr/fr/teams/network-dynamics-and-computations",
    "Aleksandra Walczak": "https://sites.google.com/view/statbiophysens",
    "Jonathan Pillow": "https://collaborate.princeton.edu/en/persons/jonathan-william-pillow/",
    "Claudia Clopath": "https://www.imperial.ac.uk/people/c.clopath",
}

# Where the "Apply" button points. The IESC runs online registration for its
# meetings; replace with the event-specific link once the IESC page exists.
APPLY_URL = "https://iesc.universita.corsica/"

# Single page: menu entries scroll to these section ids
NAV = [("about", "About"), ("organizers", "Organizers"), ("themes", "Themes"),
       ("speakers", "Speakers"), ("format", "Format"), ("venue", "Venue"), ("apply", "Apply")]

E = html.escape


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def initials(name):
    parts = [p for p in re.split(r"[\s-]+", name) if p]
    return (parts[0][0] + parts[-1][0]).upper()


def person(name, inst, tag=None):
    t = f'<span class="tag">{E(tag)}</span>' if tag else ""
    face = (f'<div class="avatar" aria-hidden="true">{initials(name)}'
            f'<img src="img/people/{slug(name)}.jpg" alt="" loading="lazy" onerror="this.remove()"></div>'
            f'<div class="name">{E(name)}</div>')
    url = URLS.get(name)
    if url:
        face = f'<a class="person-link" href="{E(url)}" target="_blank" rel="noopener">{face}</a>'
    return f'<li class="person">{face}<div class="inst">{E(inst)}</div>{t}</li>'


HEAD_JS = """<script>try{if(localStorage.getItem("theme")==="dark")document.documentElement.dataset.theme="dark"}catch(e){}</script>"""

FOOT_JS = """<script>
(function () {
  var root = document.documentElement, btn = document.querySelector(".theme-toggle");
  function label() { btn.setAttribute("aria-label", root.dataset.theme === "dark" ? "Switch to white background" : "Switch to dark background"); }
  label();
  btn.addEventListener("click", function () {
    var dark = root.dataset.theme !== "dark";
    if (dark) root.dataset.theme = "dark"; else delete root.dataset.theme;
    try { localStorage.setItem("theme", dark ? "dark" : "light"); } catch (e) {}
    label();
  });
})();
</script>"""


def page(body, hero=""):
    nav = "".join(f'<li><a href="#{i}">{E(label)}</a></li>' for i, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(TITLE)} · {E(SUBTITLE)}</title>
<meta name="description" content="{E(TITLE)}: {E(SUBTITLE)}. A residential conference at the {E(VENUE)}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{HEAD_JS}
</head>
<body id="top">
<header class="site-header"><div class="wrap">
<a class="brand" href="#top"><strong>{E(TITLE)}</strong><span>{E(SUBTITLE)}</span></a>
<div class="header-right">
<nav aria-label="Main"><ul>{nav}</ul></nav>
<button class="theme-toggle" type="button" aria-label="Switch to dark background" title="Switch background">
<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
</button>
</div>
</div></header>
{hero}
<main><div class="wrap">
{body}
</div></main>
<footer class="site-footer"><div class="wrap">
<span>{E(TITLE)} · {E(VENUE)}</span>
<span><a href="https://iesc.universita.corsica/">IESC website</a></span>
</div></footer>
{FOOT_JS}
</body>
</html>
"""


HERO = f"""<section class="hero"><div class="wrap">
<p class="kicker">International conference · 10 days</p>
<h1>{E(SUBTITLE)}</h1>
<p class="lead">A residential meeting that brings together theorists from mathematics, physics,
statistics, computer science and neuroscience to work on the mathematical foundations of neural computation.</p>
<ul class="facts">
<li><span>Where</span>{E(VENUE)}</li>
<li><span>When</span>{E(DATES)}</li>
<li><span>Format</span>Lectures, seminars, posters, discussion</li>
</ul>
</div></section>"""

ABOUT = """<section id="about"><h2>About the conference</h2>
<p>New recording technologies now capture the activity of tens of thousands of neurons at once, across
brain regions and over weeks of behaviour. Our theoretical frameworks have not kept pace: turning these
data into an understanding of how the brain computes requires new ideas from mathematics, statistics,
physics and computer science.</p>
<p>This conference creates a space for in-depth, mathematically explicit exchange between theorists who
usually work in separate communities. The programme emphasises methods, guarantees and transfer across
systems, with time to work through assumptions and derivations, not only results.</p></section>
"""

THEMES = """<section id="themes"><h2>Scientific themes</h2>
<p>The meeting is organised around five connected axes, each covered over two days.</p>
<ul class="themes">
<li><strong>Geometry of population activity</strong><span>Manifolds, dimensionality and alignment of neural representations across tasks and individuals.</span></li>
<li><strong>Latent-variable and statistical models</strong><span>State-space models, variational inference and identifiability for high-dimensional neural time series.</span></li>
<li><strong>Theory of computing circuits</strong><span>Dynamical mean-field theory, structured connectivity and control theory of recurrent networks.</span></li>
<li><strong>Theory of learning</strong><span>Statistical physics of learning, learning under biological constraints, learning regimes.</span></li>
<li><strong>NeuroAI</strong><span>Deep networks as computational hypotheses and comparisons of artificial and biological representations.</span></li>
</ul></section>
"""

FORMAT = """<section id="format"><h2>Format</h2>
<table class="schedule">
<tr><th>Mornings</th><td>Two-hour chalkboard lectures that work through derivations and algorithms in detail.</td></tr>
<tr><th>Afternoons</th><td>Research seminars on the day's theme, including contributed talks selected from participant abstracts.</td></tr>
<tr><th>Late afternoons</th><td>Poster sessions with whiteboards, a mentorship session across career stages, and a daily closing round table on the future of theoretical neuroscience in the age of AI.</td></tr>
<tr><th>Participants</th><td>About 65 in total: invited speakers and around 40 PhD students, postdocs and early-career researchers selected by application.</td></tr>
</table></section>
"""

VENUE_SECTION = """<section id="venue"><h2>Venue</h2>
<figure class="venue"><img src="img/venue.jpg" alt="The Institut d'Études Scientifiques de Cargèse, on a green hillside above the sea" width="678" height="452" loading="lazy"><figcaption>The Institut d'Études Scientifiques de Cargèse.</figcaption></figure>
<figure class="video"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/OmZZhEgi4wo" title="Présentation de l'IES Cargèse (video)" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><figcaption>Video presentation of the institute by the IESC. <a href="https://www.youtube.com/watch?v=OmZZhEgi4wo">Watch on YouTube</a>.</figcaption></figure>
<p>The conference takes place at the Institut d'Études Scientifiques de Cargèse (IESC), a residential
institute on the west coast of Corsica, about an hour by road from Ajaccio airport. Participants are housed
on site or in the village, and lunches are taken together at the institute.</p>
<p class="muted">Dates, registration fees and travel information will be posted here once confirmed.</p></section>
"""


# Placeholder cards so the speaker grid ends on a full row (5 per row on desktop)
ROW = 5
SILHOUETTE = ('<svg class="silhouette" viewBox="0 0 64 64" aria-hidden="true">'
              '<circle cx="32" cy="24" r="12"/><path d="M8 60c2-14 12-22 24-22s22 8 24 22z"/></svg>')


def tbc_card():
    return (f'<li class="person tbc"><div class="avatar" aria-hidden="true">{SILHOUETTE}</div>'
            '<div class="name">To be confirmed</div><div class="inst">Speaker to be announced</div></li>')


def speakers_body():
    items = "".join(person(n, i, t) for n, i, t in SPEAKERS)
    items += tbc_card() * ((-len(SPEAKERS)) % ROW)
    return f"""<section id="speakers"><h2>Speakers</h2>
<p>Lecturers and seminar speakers confirmed so far. The list will be updated as further speakers confirm.</p>
<ul class="people">{items}</ul></section>
"""


def organizers_body():
    items = "".join(person(n, i) for n, i in ORGANIZERS)
    committee = "".join(person(n, i) for n, i in SCIENTIFIC_COMMITTEE)
    return f"""<section id="organizers"><h2>Organizers</h2>
<ul class="people">{items}</ul>
<h3 class="subhead">Scientific committee</h3>
<ul class="people">{committee}</ul>
<h3 class="subhead">Contact</h3>
<p>For questions about the scientific programme, please contact the organizers. Practical questions about
accommodation and travel are handled by the <a href="https://iesc.universita.corsica/">IESC</a>.</p></section>
"""


def apply_body():
    return f"""<section id="apply"><h2>Apply to attend</h2>
<p>About 40 places are open to PhD students, postdocs and early-career researchers.
<strong>All participants must present their work, either as a poster or as a contributed talk.</strong></p>
<div class="note">Applications are not open yet. The call, deadline and selection dates will be announced on this page.</div>

<h3>Who should apply</h3>
<p>Researchers with a strong background in a quantitative discipline (mathematics, physics, statistics,
computer science or computational neuroscience) who work on, or want to work on, theory and data analysis
for neural systems.</p>

<h3>How to apply</h3>
<ol class="steps">
<li>Prepare a short CV and a one-paragraph statement explaining how the conference relates to your work.</li>
<li>Prepare an abstract (up to 300 words) for your poster or contributed talk, and indicate which format you prefer.</li>
<li>Submit your application through the IESC online registration system once the call opens.</li>
</ol>

<h3>Selection</h3>
<p>Participants are selected by the organizers for technical strength and fit with the programme, and for
diversity of research area, career stage, institution and geography. Contributed talks are chosen from
submitted abstracts. We aim for a gender-balanced meeting.</p>

<h3>Financial support</h3>
<p>We are seeking funding to support participants, with priority for early-career researchers and for
applicants from countries with limited research funding. Details will be given with the call.</p>

<p><a class="button" href="{E(APPLY_URL)}">Go to the IESC registration site</a></p></section>
"""


REDIRECT = """<!doctype html><meta charset="utf-8"><title>{t}</title>
<meta http-equiv="refresh" content="0; url=index.html#{a}"><link rel="canonical" href="index.html#{a}">
<p><a href="index.html#{a}">{t}</a></p>
"""


def main():
    body = (ABOUT + organizers_body() + THEMES + speakers_body() + FORMAT + VENUE_SECTION + apply_body())
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(body, HERO))
    # Old multi-page URLs now point to the matching section
    for name, anchor in [("speakers", "speakers"), ("organizers", "organizers"), ("apply", "apply")]:
        with open(os.path.join(ROOT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(REDIRECT.format(t=E(TITLE), a=anchor))
    print("Built: index.html (+ redirects)")


if __name__ == "__main__":
    main()
