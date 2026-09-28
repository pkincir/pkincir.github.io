# Pelin Kıncır: personal website

Source of Pelin Kıncır's homepage, based on [Michael Niemeyer's homepage template](https://github.com/m-niemeyer/m-niemeyer.github.io) (MIT license, see `LICENSE.md`). `build.py` reads the `.bib` files and writes `index.html`. That file plus `assets/` is the whole site.

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install pybtex
.venv/bin/python build.py
```

Then open `index.html` in a browser. The build prints a line for every figure or photo that is still missing.

## What to edit

| What | Where |
|---|---|
| Name, bio, links, awards, footer | `get_personal_data()` in `build.py` |
| Profile photo | Save it as `assets/img/profile.jpg` (portrait, 2:3). A placeholder is shown until the file exists. |
| Research projects | `project_list.bib`, shown from top to bottom |
| Project figures | Each project's `img` field points to a file in `assets/img/projects/` (`arlab.jpg`, `teng.mp4`, `so101_typer.jpg`, `sceneflow.mp4`, `voxelwarping.jpg`, `network_coding.jpg`). Save the figure under that name, or change the path, and rebuild. `.png`, `.gif` and `.mp4` work too. |
| Project links | Optional `html`, `pdf`, `slides`, `poster`, `video` and `code` fields in a project entry, shown as [Project Page] [Report] [Slides] [Poster] [Video] [Code] |
| Publications | `publication_list.bib`, shown above the projects. Entries are text-only unless they have an `img` field (a thumbnail path, e.g. `assets/img/publications/teng_paper.jpg`). Entries with a `pubstate` field (e.g. `submitted`) are shown without the bibtex block. |
| Talks | Create `talk_list.bib` (same format as in the template) and a Talks section appears. |
| CV and reports | `assets/pdf/` (the reports are linked through the `pdf` field of their project) |

## Credits

Template by [Michael Niemeyer](https://m-niemeyer.github.io/), which in turn is inspired by [Jon Barron's website](https://jonbarron.info/).

## Publishing

The GitHub account is `pkincir`, and the website repository is `pkincir.github.io`.
In GitHub Settings → Pages, publish from the `main` branch and `/ (root)`.
The public address is https://pkincir.github.io/ once deployment completes.
The `.nojekyll` file lets GitHub serve the already-generated HTML directly.

The same `index.html` and `assets/` work at https://people.ee.ethz.ch/~pkincir/.
Connect with `ssh pkincir@login.ee.ethz.ch`, back up any existing website, and place
these files in `~/public_html/`. Keep the asset directory structure unchanged.
The web server needs traversal permission on the home and website directories,
and read permission on public website files, as described in the D-ITET tutorial.
Python and the build environment are only needed locally; do not upload `.venv/`
or `.git/` to the ETH web folder.

For future edits, change `build.py` or the `.bib` files, rebuild `index.html`,
and publish the updated HTML and assets to both hosts.
