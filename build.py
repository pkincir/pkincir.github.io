import html
import os

from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Pelin", "Kıncır"]
    email = "pkincir@mit.edu"
    email_eth = "pkincir@ethz.ch"
    github = "pkincir"
    linkedin = "pelin-k%C4%B1nc%C4%B1r-992779190"
    bio_text = f"""
                <p>
                    I am a Master's student in Electrical Engineering and Information Technology at <a href="https://ethz.ch/en.html" target="_blank">ETH Zurich</a>, specializing in Signal Processing and Machine Learning.
                    For my thesis, I am a visiting researcher (MIT affiliate) at the <a href="https://www.broadinstitute.org/" target="_blank">Broad Institute of MIT and Harvard</a> with Prof. Giovanni Traverso, developing an AI-powered AR assistant for wet-lab procedures on Apple Vision Pro.
                    I hold a B.Sc. in Electrical and Electronics Engineering from <a href="https://bogazici.edu.tr/en" target="_blank">Boğaziçi University</a>.
                </p>
                <p>
                    My research focuses on 3D perception and multimodal systems that assist people in physical environments, spanning dynamic 3D reconstruction, robotic mapping, wearable sensing, and AR.
                </p>
                <p>Feel free to reach out to me at <a href="mailto:{email}">{email}</a> or <a href="mailto:{email_eth}">{email_eth}</a>.</p>
                <p>
                    <a href="assets/other/bio.txt" target="_blank" style="margin-right: 5px; white-space: nowrap;"><i class="fa-solid fa-graduation-cap"></i> Bio</a>
                    <a href="{versioned('assets/pdf/CV_Pelin_Kincir.pdf')}" target="_blank" style="margin-right: 5px; white-space: nowrap;"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" style="margin-right: 5px; white-space: nowrap;"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 5px; white-space: nowrap;"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="https://www.linkedin.com/in/{linkedin}/" target="_blank" style="margin-right: 5px; white-space: nowrap;"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#awards" aria-expanded="false" aria-controls="awards" style="margin-left: -6px; margin-top: -2px;"><i class="fa-solid fa-trophy"></i> Awards</button>
                </p>
                <div id="awards" class="collapse">
                    <span style="font-weight: bold;">Awards:</span>
                    In 2026, I received a Heyning-Roelli Foundation Scholarship, which supports my Master's thesis research exchange at the Broad Institute of MIT and Harvard.
                    From 2023 to 2024, I was a TÜBİTAK Undergraduate Research Fellow; the fellowship supported my B.Sc. senior design project.
                </div>
    """
    footer = """
            <div class="col-sm-12" style="">
                <p style="color: #6c757d; font-size: 0.9em;">
                    Website template by <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a>
                    (<a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">source</a>).
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    # Co-author name (as written in the bib file) -> website, e.g. 'Jane Doe': 'https://janedoe.github.io/'
    return {
        }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='P. Kincir', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = " ".join(p.get_part('first') + p.get_part('middle') + p.get_part('prelast') + p.get_part('last'))
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold;">{make_bold_name}</span>'
        elif string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_links_html(entry, artefacts):
    links = []
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            url = entry.fields[k]
            if os.path.exists(url):  # local file such as a report PDF
                url = versioned(url)
            links.append(f"""<a href="{url}" target="_blank">[{v}]</a>""")
    return ' '.join(links)

def versioned(path):
    # The ?v=<modification time> suffix makes browsers load a changed file instead of a cached copy
    return f"{path}?v={int(os.path.getmtime(path))}"

def get_media_html(entry_key, entry):
    path = entry.fields['img'] if 'img' in entry.fields.keys() else ''
    if path and os.path.exists(path):
        if path.lower().endswith(('.mp4', '.webm')):
            return f"""<video src="{versioned(path)}" class="img-fluid img-thumbnail" autoplay loop muted playsinline></video>"""
        return f"""<img src="{versioned(path)}" class="img-fluid img-thumbnail" alt="{html.escape(entry.fields['title'])}">"""
    print(f'[{entry_key}] Figure {path or "(no img field)"} not found, showing a placeholder.')
    return """<div class="img-thumbnail placeholder-box"><i class="fa-regular fa-image"></i>Figure coming soon</div>"""

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row">"""
    if 'img' in entry.fields.keys():
        s += """<div class="col-sm-4">"""
        s += get_media_html(entry_key, entry)
        s += """</div><div class="col-sm-8">"""
    else:
        s += """<div class="col-sm-12">"""

    if 'html' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a>"""
    else:
        s += f"""<span style="font-weight: bold;">{entry.fields['title']}</span>"""
    if 'award' in entry.fields.keys():
        s += f""" <span style="color: red;">({entry.fields['award']})</span>"""
    s += """<br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    venue = entry.fields['booktitle'] if 'booktitle' in entry.fields.keys() else entry.fields['journal']
    if 'pubstate' in entry.fields.keys():
        venue += f" ({entry.fields['pubstate']})"
    s += f"""<span style="font-style: italic;">{venue}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    links = get_links_html(entry, artefacts)
    s += links

    # Papers that are not out yet (pubstate = submitted, ...) get no bibtex block
    if 'pubstate' not in entry.fields.keys():
        cite = "<pre><code>@" + f"{entry.type}" + "{" + f"{entry_key}, \n"
        cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
        for entr in ['title', 'booktitle', 'journal', 'year']:
            if entr in entry.fields.keys():
                cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
        cite += """}</code></pre>"""
        s += (" " if links else "") + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapse{entry_key}" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_project_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-4">"""
    s += get_media_html(entry_key, entry)
    s += """</div><div class="col-sm-8">"""

    if 'html' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""
    else:
        s += f"""<span style="font-weight: bold;">{entry.fields['title']}</span> <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['category']}</span>, {entry.fields['institution']} <br>"""
    s += f"""{entry.fields['date']}"""
    if 'supervisor' in entry.fields.keys():
        s += f""", supervised by {entry.fields['supervisor']}"""
    s += """ <br>"""
    s += f"""<p style="margin-top: 0.5em; margin-bottom: 0.5em;">{entry.fields['description']}</p>"""
    if 'skills' in entry.fields.keys():
        skills = ' · '.join(skill.strip() for skill in entry.fields['skills'].split(','))
        s += f"""<span style="color: #6c757d; font-size: 0.9em;">{skills}</span> <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Report', 'slides': 'Slides', 'poster': 'Poster', 'video': 'Video', 'code': 'Code'}
    s += get_links_html(entry, artefacts)
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-4">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-8">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_entries_html(filename, get_entry):
    # Sections whose bib file is missing or empty are left out of the page
    if not os.path.exists(filename):
        return ""
    parser = bibtex.Parser()
    bib_data = parser.parse_file(filename)
    s = ""
    for k in bib_data.entries.keys():
        s += get_entry(k, bib_data.entries[k])
    return s

def get_profile_html(path='assets/img/profile.jpg'):
    if os.path.exists(path):
        return f"""<img src="{versioned(path)}" class="img-thumbnail profile-img" width="280px" alt="Profile picture">"""
    print(f'Profile photo {path} not found, showing a placeholder.')
    return """<div class="img-thumbnail placeholder-box profile-placeholder"><i class="fa-solid fa-user"></i></div>"""

def get_index_html():
    projects = get_entries_html('project_list.bib', get_project_entry)
    pub = get_entries_html('publication_list.bib', get_paper_entry)
    talks = get_entries_html('talk_list.bib', get_talk_entry)
    name, bio_text, footer = get_personal_data()

    sections = ""
    for (title, content) in [('Publications', pub), ('Research Projects', projects), ('Talks', talks)]:
        if content:
            sections += f"""
                <div class="row" style="margin-top: {'1em' if sections == '' else '3em'};">
                    <div class="col-sm-12" style="">
                        <h4>{title}</h4>
                        {content}
                    </div>
                </div>"""

    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="{name[0] + ' ' + name[1]}: Master's student at ETH Zurich working on computer vision, 3D perception, and AR.">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <style>
    .placeholder-box {{
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      width: 100%; aspect-ratio: 16 / 10;
      background-color: #f1f3f5; color: #adb5bd; font-size: 0.85em;
    }}
    .placeholder-box i {{ font-size: 2em; margin-bottom: 0.4em; }}
    .profile-placeholder {{ aspect-ratio: 2 / 3; max-width: 280px; }}
    .profile-placeholder i {{ font-size: 3em; }}
    /* 1.5x the width the photo had in the template's col-md-2 column */
    @media (min-width: 768px) {{
      .profile-img {{ display: block; width: calc(100% - 15px); margin-left: auto; }}
    }}
  </style>

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-9" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-3" style="">
                        {get_profile_html()}
                    </div>
                </div>
                {sections}
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
            <div class="col-md-1"></div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')
