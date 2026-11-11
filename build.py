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
    ("Zachary Kilpatrick", "University of Colorado Boulder", "Neural circuits"),
    ("Francesca Mastrogiuseppe", "Champalimaud Foundation", "Neural circuits"),
    ("Leenoy Meshulam", "Brown University", "Neural circuits"),
    ("Yonathan Aljadeff", "UC San Diego", "Neural circuits"),
    ("Francesca Mignacco", "Princeton University", "Learning"),
    ("Sebastian Goldt", "SISSA, Trieste", "Learning"),
    ("Samuel Muscinelli", "University of Chicago", "Learning"),
    ("Dan Levenstein", "Yale University", "NeuroAI"),
    ("Ulises Pereira", "Allen Institute", "NeuroAI"),
]

ORGANIZERS = [
    ("Joao Barbosa", "Neuromodulation Institute, INSERM, France"),
    ("Lea Duncker", "Columbia University, USA"),
    ("Lorenzo Fontolan", "INMED, INSERM, France"),
    ("Agostina Palmigiano", "Gatsby Computational Neuroscience Unit, UCL, UK"),
    ("Lorenzo Posani", "Paris Brain Institute, CNRS, France"),
]

# Where the "Apply" button points. The IESC runs online registration for its
# meetings; replace with the event-specific link once the IESC page exists.
APPLY_URL = "https://iesc.universita.corsica/"

PAGES = [("index.html", "About"), ("speakers.html", "Speakers"),
         ("organizers.html", "Organizers"), ("apply.html", "Apply")]

E = html.escape


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def initials(name):
    parts = [p for p in re.split(r"[\s-]+", name) if p]
    return (parts[0][0] + parts[-1][0]).upper()


def person(name, inst, tag=None):
    t = f'<span class="tag">{E(tag)}</span>' if tag else ""
    return (f'<li class="person"><div class="avatar" aria-hidden="true">{initials(name)}'
            f'<img src="img/people/{slug(name)}.jpg" alt="" loading="lazy" onerror="this.remove()"></div>'
            f'<div class="name">{E(name)}</div><div class="inst">{E(inst)}</div>{t}</li>')


def page(filename, title, body, hero=""):
    nav = "".join(
        f'<li><a href="{f}"{" aria-current=\"page\"" if f == filename else ""}>{E(label)}</a></li>'
        for f, label in PAGES)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} · {E(TITLE)}</title>
<meta name="description" content="{E(TITLE)}: {E(SUBTITLE)}. A residential conference at the {E(VENUE)}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="brand" href="index.html"><strong>{E(TITLE)}</strong><span>{E(SUBTITLE)}</span></a>
<nav aria-label="Main"><ul>{nav}</ul></nav>
</div></header>
{hero}
<main><div class="wrap">
{body}
</div></main>
<footer class="site-footer"><div class="wrap">
<span>{E(TITLE)} · {E(VENUE)}</span>
<span><a href="https://iesc.universita.corsica/">IESC website</a></span>
</div></footer>
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

ABOUT = """<h2>About the conference</h2>
<p>New recording technologies now capture the activity of tens of thousands of neurons at once, across
brain regions and over weeks of behaviour. Our theoretical frameworks have not kept pace: turning these
data into an understanding of how the brain computes requires new ideas from mathematics, statistics,
physics and computer science.</p>
<p>This conference creates a space for in-depth, mathematically explicit exchange between theorists who
usually work in separate communities. The programme emphasises methods, guarantees and transfer across
systems, with time to work through assumptions and derivations, not only results.</p>

<h2>Scientific themes</h2>
<p>The meeting is organised around five connected axes, each covered over two days.</p>
<ul class="themes">
<li><strong>Geometry of population activity</strong><span>Manifolds, dimensionality and alignment of neural representations across tasks and individuals.</span></li>
<li><strong>Latent-variable and statistical models</strong><span>State-space models, variational inference and identifiability for high-dimensional neural time series.</span></li>
<li><strong>Theory of computing circuits</strong><span>Dynamical mean-field theory, structured connectivity and control theory of recurrent networks.</span></li>
<li><strong>Theory of learning</strong><span>Statistical physics of learning, learning under biological constraints, learning regimes.</span></li>
<li><strong>NeuroAI</strong><span>Deep networks as computational hypotheses and comparisons of artificial and biological representations.</span></li>
</ul>

<h2>Format</h2>
<table class="schedule">
<tr><th>Mornings</th><td>Two-hour chalkboard lectures that work through derivations and algorithms in detail.</td></tr>
<tr><th>Afternoons</th><td>Research seminars on the day's theme, including contributed talks selected from participant abstracts.</td></tr>
<tr><th>Late afternoons</th><td>Poster sessions with whiteboards, a mentorship session across career stages, and a closing round table on the future of theoretical neuroscience.</td></tr>
<tr><th>Participants</th><td>About 65 in total: invited speakers and around 40 PhD students, postdocs and early-career researchers selected by application.</td></tr>
</table>

<h2>Venue</h2>
<p>The conference takes place at the Institut d'Études Scientifiques de Cargèse (IESC), a residential
institute on the west coast of Corsica, about an hour by road from Ajaccio airport. Participants are housed
on site or in the village, and lunches are taken together at the institute.</p>
<p class="muted">Dates, registration fees and travel information will be posted here once confirmed.</p>
"""


def speakers_body():
    items = "".join(person(n, i, t) for n, i, t in SPEAKERS)
    return f"""<h2>Confirmed speakers</h2>
<p>Lecturers and seminar speakers confirmed so far. The list will be updated as further speakers confirm.</p>
<ul class="people">{items}</ul>
"""


def organizers_body():
    items = "".join(person(n, i) for n, i in ORGANIZERS)
    return f"""<h2>Organizers</h2>
<p>The conference is organised by five group leaders working on the mathematical foundations of neural
computation, across geometry of representations, statistical methods, circuit dynamics and NeuroAI.</p>
<ul class="people">{items}</ul>
<h2>Contact</h2>
<p>For questions about the scientific programme, please contact the organizers. Practical questions about
accommodation and travel are handled by the <a href="https://iesc.universita.corsica/">IESC</a>.</p>
"""


def apply_body():
    return f"""<h2>Apply to attend</h2>
<p>About 40 places are open to PhD students, postdocs and early-career researchers. Applicants can
request to present a poster or a contributed talk.</p>
<div class="note">Applications are not open yet. The call, deadline and selection dates will be announced on this page.</div>

<h3>Who should apply</h3>
<p>Researchers with a strong background in a quantitative discipline (mathematics, physics, statistics,
computer science or computational neuroscience) who work on, or want to work on, theory and data analysis
for neural systems.</p>

<h3>How to apply</h3>
<ol class="steps">
<li>Prepare a short CV and a one-paragraph statement explaining how the conference relates to your work.</li>
<li>Prepare an abstract (up to 300 words) if you would like to present a poster or a contributed talk, and indicate your preference.</li>
<li>Submit your application through the IESC online registration system once the call opens.</li>
</ol>

<h3>Selection</h3>
<p>Participants are selected by the organizers for technical strength and fit with the programme, and for
diversity of research area, career stage, institution and geography. Contributed talks are chosen from
submitted abstracts. We aim for a gender-balanced meeting.</p>

<h3>Financial support</h3>
<p>We are seeking funding to support participants, with priority for early-career researchers and for
applicants from countries with limited research funding. Details will be given with the call.</p>

<p><a class="button" href="{E(APPLY_URL)}">Go to the IESC registration site</a></p>
"""


def main():
    out = {
        "index.html": page("index.html", "About", ABOUT, HERO),
        "speakers.html": page("speakers.html", "Speakers", speakers_body()),
        "organizers.html": page("organizers.html", "Organizers", organizers_body()),
        "apply.html": page("apply.html", "Apply", apply_body()),
    }
    for name, content in out.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("Built:", ", ".join(out))


if __name__ == "__main__":
    main()
