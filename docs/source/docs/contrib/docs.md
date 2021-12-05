We use [MkDocs](https://www.mkdocs.org/#overview) to create our documentation.

For more information beyond what is in this guide, check out the [MkDocs](https://www.mkdocs.org/#getting-started) and [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) documentation.

---

## Setting Up the Environment

1. Install `Python 3.x`
2. Fork `Conreq:develop` from GitHub.
3. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
4. Type `pip install -r requirements.txt` to install MkDocs.

---

## Starting the Docs Preview Webserver

1. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
2. Type `python manage.py serve_docs` to start the preview webserver.
3. Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the documentation and changes live!

---

## Adding/Editing a Docs Page

1. Create a new markdown file within `Conreq/docs/source/`, or edit an existing markdown file within this folder.
2. Fill in this file with any markdown text you want!
3. _If you made a new file,_ add this docs page to the navigation by editing `Conreq/docs/source/mkdocs.yml`.
4. Commit your changes to your GitHub branch.
5. Submit a GitHub pull request to `Archmonger/Conreq:develop`.

---

## Building the Docs

This section is intended for Conreq repository leaders.

1. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
2. Type `python manage.py build_docs` to turn the preview into something we can use.
