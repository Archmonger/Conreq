We use [MkDocs](https://www.mkdocs.org/#overview) to create our documentation. For more information beyond what is in this guide, check out the [MkDocs Documentation](https://www.mkdocs.org/#getting-started).

---

### Setting up the Docs Environment

---

1. Install Python 3.8+
2. Switch your Conreq branch to `Conreq:docs`
3. Type `pip install -r requirements.txt` to install MkDocs via Python.

---

### Starting the Preview Webserver

---

MkDocs contains a free tool to allow you to preview your documentation changes live! In order to use it...

1. Type `mkdocs serve` to start the preview webserver
2. Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the documentation and changes live!

---

### Adding a New Docs Page

---

1. Create a new markdown file within `docs/`
2. Fill in this file with any markdown text you want!
3. Add this file to the navigation bar within `mkdocs.yml`

---

### Saving Your Changes

---

At this point you've successfully created a new docs page, and determine you want to contribute these changes. In order to do so...

1. Type `mkdocs build` to turn the preview into something we can use
2. Commit your changes to GitHub
3. Submit a Pull Request to Conreq's repository
