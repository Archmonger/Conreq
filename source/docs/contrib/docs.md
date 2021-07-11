We use [MkDocs](https://www.mkdocs.org/#overview) to create our documentation. For more information beyond what is in this guide, check out the [MkDocs Documentation](https://www.mkdocs.org/#getting-started).

---

## Setting Up the Environment

1. Install `Python 3.8` or greater.
2. Fork and pull `Conreq:docs` from GitHub.
3. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
4. Type `pip install -r requirements.txt` to install MkDocs.

---

## Starting the Preview Webserver

MkDocs contains a tool to allow you to preview your documentation changes live! In order to use it...

1. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
2. Type `cd source` to enter the documentation's source code directory.
3. Type `mkdocs serve` to start the preview webserver.
4. Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the documentation and changes live!

---

## Adding/Editing a Docs Page

1. Create a new markdown file within `source/docs/`, or edit an existing markdown file.
2. Fill in this file with any markdown text you want!
3. _If you made a new file:_ Add this file to the navigation bar within `mkdocs.yml`.

---

## Contributing Your Changes

At this point you've successfully created a new docs page, and determine you want to contribute these changes. In order to do so...

1. Open a terminal (ex. Command Prompt or PowerShell) at the root of the repository.
2. Type `cd source` to enter the documentation's source code directory.
3. Type `mkdocs build -d ..\docs` to turn the preview into something we can use.
4. Commit your changes to your GitHub branch.
5. Submit a GitHub pull request to `Archmonger/Conreq:docs`.
