# Cargèse 2029 conference website

A static website for the Cargèse 2029 conference on theoretical neuroscience: plain HTML and one CSS file, with no frameworks and no build dependencies beyond Python 3.

## Pages

- `index.html`: about, scientific themes, format and venue
- `speakers.html`: confirmed speakers
- `organizers.html`: organizing committee and contact
- `apply.html`: how to apply for a poster or contributed talk

## Editing

All content lives in `build.py`. Edit the speaker and organizer lists or the texts there, then regenerate the pages:

```bash
python3 build.py
```

## Photos

Add a square JPEG (about 400×400 px) for each person at `img/people/<slug>.jpg`, where the slug is the name in lowercase with hyphens and no accents, for example `img/people/pedro-goncalves.jpg`. People without a photo are shown with their initials. Ask each speaker for a photo they are happy to have published.

## Publishing with GitHub Pages

In the repository settings on GitHub, open **Pages**, set the source to **Deploy from a branch**, choose `main` and the root folder, and save. The site will be available at `https://jmourabarbosa.github.io/cargese-neuro29/`.
