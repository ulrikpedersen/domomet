Search.setIndex({"docnames": ["developer/explanations/decisions", "developer/explanations/decisions/0001-record-architecture-decisions", "developer/how-to/build-docs", "developer/how-to/contribute", "developer/how-to/lint", "developer/how-to/make-release", "developer/how-to/pin-requirements", "developer/how-to/run-tests", "developer/how-to/static-analysis", "developer/how-to/test-container", "developer/how-to/update-tools", "developer/index", "developer/reference/standards", "developer/tutorials/dev-install", "genindex", "index", "user/explanations/docs-structure", "user/how-to/run-container", "user/index", "user/reference/api", "user/tutorials/installation"], "filenames": ["developer/explanations/decisions.rst", "developer/explanations/decisions/0001-record-architecture-decisions.rst", "developer/how-to/build-docs.rst", "developer/how-to/contribute.rst", "developer/how-to/lint.rst", "developer/how-to/make-release.rst", "developer/how-to/pin-requirements.rst", "developer/how-to/run-tests.rst", "developer/how-to/static-analysis.rst", "developer/how-to/test-container.rst", "developer/how-to/update-tools.rst", "developer/index.rst", "developer/reference/standards.rst", "developer/tutorials/dev-install.rst", "genindex.rst", "index.rst", "user/explanations/docs-structure.rst", "user/how-to/run-container.rst", "user/index.rst", "user/reference/api.rst", "user/tutorials/installation.rst"], "titles": ["Architectural Decision Records", "1. Record architecture decisions", "Build the docs using sphinx", "Contributing to the project", "Run linting using pre-commit", "Make a release", "Pinning Requirements", "Run the tests using pytest", "Run static analysis using mypy", "Container Local Build and Test", "Update the tools", "Developer Guide", "Standards", "Developer install", "API Index", "domomet", "About the documentation", "Run in a container", "User Guide", "API", "Installation"], "terms": {"we": [0, 1, 3, 6], "major": 0, "adr": [0, 1], "describ": [0, 1], "michael": [0, 1], "nygard": [0, 1], "below": 0, "i": [0, 3, 4, 6, 7, 8, 9, 10, 11, 12, 16, 18, 19, 20], "list": [0, 6], "our": 0, "current": [0, 10, 20], "1": [0, 12], "date": 1, "2022": 1, "02": 1, "18": 1, "accept": 1, "need": [1, 6, 16, 20], "made": [1, 6], "thi": [1, 2, 4, 5, 6, 9, 10, 12, 13, 15, 16, 19, 20], "project": [1, 2, 6, 7, 9, 10, 11], "us": [1, 6, 11, 12, 13, 15, 17, 20], "see": [1, 2, 5], "": 1, "articl": 1, "link": [1, 11, 18], "abov": [1, 4], "To": [1, 5, 6, 9, 10, 13, 17], "creat": [1, 5, 6], "new": [1, 3, 5, 13, 18], "copi": [1, 6], "past": 1, "from": [1, 2, 11, 12, 15, 17, 18, 20], "exist": [1, 3, 20], "ones": 1, "you": [2, 3, 4, 5, 6, 7, 8, 9, 13, 15, 20], "can": [2, 3, 4, 6, 7, 8, 9, 13, 20], "base": 2, "directori": [2, 12], "run": [2, 3, 9, 10, 11, 12, 13, 18], "tox": [2, 4, 7, 8, 9, 13], "e": [2, 4, 6, 7, 8, 13], "static": [2, 11, 12, 13], "which": [2, 9, 10, 13], "includ": [2, 18], "api": [2, 12, 18], "pull": [2, 3, 10, 17], "docstr": [2, 12], "code": [2, 4, 15], "document": [2, 3, 11, 18], "standard": [2, 3, 11], "The": [2, 3, 4, 6, 9, 12, 15, 16, 20], "built": [2, 17], "html": 2, "open": [2, 3, 13], "local": [2, 11, 13], "web": 2, "brows": 2, "firefox": 2, "index": [2, 18], "also": [2, 3, 7, 11, 18, 20], "an": [2, 4, 6, 10], "process": [2, 12], "watch": 2, "your": [2, 3, 6, 9], "chang": [2, 3, 4, 6, 10, 15], "rebuild": 2, "whenev": 2, "reload": 2, "ani": [2, 3, 4, 6, 9, 10, 20], "browser": 2, "page": [2, 5, 6, 12], "view": 2, "localhost": 2, "http": [2, 5, 10, 15, 20], "8000": 2, "If": [2, 3, 4, 9, 20], "ar": [2, 3, 6, 12, 16, 17], "make": [2, 3, 11], "sourc": [2, 8, 13, 15, 20], "too": 2, "tell": [2, 4], "src": 2, "most": [3, 16], "welcom": 3, "all": [3, 4, 6, 9], "request": [3, 10], "handl": [3, 4], "through": [3, 13], "github": [3, 5, 10, 13, 15, 17, 20], "pleas": [3, 5, 12], "check": [3, 4, 7, 8, 9, 10, 12, 13], "befor": 3, "file": [3, 4, 8], "one": [3, 6, 16], "have": [3, 4, 6, 9, 13], "great": 3, "idea": [3, 6], "involv": 3, "big": 3, "ticket": 3, "want": 3, "sure": 3, "don": 3, "t": [3, 9, 16], "spend": 3, "time": [3, 4, 6], "someth": [3, 10], "might": [3, 15], "fit": 3, "scope": 3, "offer": 3, "place": [3, 6], "ask": 3, "question": 3, "share": 3, "end": 3, "obviou": 3, "when": [3, 6, 13], "close": [3, 10], "rais": 3, "instead": [3, 9, 17], "while": 3, "100": 3, "doe": 3, "librari": [3, 6, 18], "bug": 3, "free": 3, "significantli": 3, "reduc": 3, "number": [3, 5, 6, 17, 19], "easili": 3, "caught": 3, "remain": 3, "same": [3, 5, 6], "improv": [3, 16], "contain": [3, 6, 11, 12, 13, 15, 18], "inform": [3, 16], "set": [3, 4, 6, 12], "up": [3, 11], "environ": [3, 6, 13], "test": [3, 6, 11], "what": 3, "should": [3, 6, 20], "follow": [3, 5, 9, 12, 13], "black": [4, 12], "flake8": [4, 12], "isort": [4, 12], "under": [4, 13], "command": [4, 9, 15], "Or": [4, 15], "instal": [4, 6, 9, 11, 15, 17, 18], "hook": 4, "each": [4, 6], "do": [4, 6, 8, 9], "git": [4, 10, 13, 15, 20], "just": 4, "report": [4, 7], "reformat": 4, "repositori": [4, 6, 12], "likewis": 4, "get": [4, 5, 6, 11, 13, 17], "those": 4, "manual": 4, "json": 4, "formatt": 4, "well": 4, "save": 4, "highlight": [4, 8], "editor": 4, "window": 4, "checklist": 5, "choos": [5, 13], "pep440": 5, "compliant": 5, "pep": 5, "python": [5, 6, 10, 13, 15], "org": 5, "0440": 5, "go": [5, 6], "draft": 5, "click": [5, 6, 13], "tag": 5, "suppli": 5, "chose": 5, "gener": [5, 10], "note": [5, 18], "review": 5, "edit": 5, "titl": [5, 12], "publish": [5, 6], "push": [5, 6], "main": [5, 17], "branch": 5, "ha": [5, 6, 10, 20], "effect": 5, "except": 5, "option": 5, "By": 6, "design": 6, "onli": 6, "defin": [6, 12], "tabl": 6, "pyproject": 6, "toml": 6, "In": [6, 9], "possibl": 6, "version": [6, 10, 15, 17, 19], "some": [6, 15], "For": [6, 12], "best": [6, 9], "leav": 6, "minimum": 6, "so": [6, 13, 20], "widest": 6, "rang": 6, "applic": [6, 9], "build": [6, 11, 12], "latest": [6, 10], "compat": 6, "avail": [6, 9, 17], "after": 6, "approach": [6, 16], "mean": [6, 10], "futur": 6, "mai": 6, "break": 6, "becaus": [6, 9], "updat": [6, 11], "releas": [6, 11, 15, 17, 18, 20], "correct": 6, "wai": [6, 18], "fix": [6, 9], "issu": [6, 8], "work": [6, 18], "out": 6, "resolv": 6, "problem": [6, 9], "howev": 6, "quit": 6, "hard": 6, "consum": 6, "simpli": 6, "try": 6, "minor": 6, "reason": 6, "provid": [6, 10], "mechan": 6, "previou": 6, "success": 6, "quick": 6, "guarante": 6, "everi": 6, "asset": 6, "exampl": [6, 9, 12, 15], "take": [6, 13], "look": [6, 7], "domomet": [6, 13, 17, 20], "cli": [6, 9], "here": [6, 15, 18], "ulrikpedersen": [6, 13, 15, 17, 20], "There": [6, 16], "txt": 6, "show": 6, "virtual": 6, "multipl": [6, 10], "differ": [6, 16], "pip": [6, 10, 13, 15, 20], "freez": 6, "full": 6, "sub": 6, "download": 6, "them": [6, 7, 8], "It": [6, 7, 8, 20], "ran": 6, "lowest": 6, "more": [6, 10, 16, 18], "like": [6, 7], "matrix": 6, "ubuntu": 6, "3": [6, 12, 13, 20], "8": [6, 13, 20], "lockfil": 6, "root": [6, 9], "renam": 6, "commit": [6, 11, 12, 13], "repo": 6, "pass": [6, 9], "exactli": 6, "packag": [6, 13], "onc": 6, "been": [6, 20], "good": [6, 16], "back": [6, 15], "unlock": 6, "earli": 6, "indic": [6, 10], "incom": 6, "restor": 6, "done": [7, 8], "find": 7, "function": [7, 12, 16], "error": 7, "coverag": 7, "commandlin": [7, 15, 20], "cov": 7, "xml": 7, "type": [8, 12, 13, 20], "definit": 8, "without": 8, "potenti": 8, "where": [8, 10], "match": 8, "ci": 9, "runtim": 9, "via": 9, "p": [9, 13], "verifi": 9, "develop": [9, 15], "docker": [9, 17], "fail": 9, "would": 9, "requir": [9, 11, 13, 16, 20], "podman": 9, "workstat": 9, "interchang": 9, "depend": [9, 17, 20], "call": [9, 16], "cd": [9, 13], "help": [9, 16], "other": 9, "line": [9, 12], "paramet": 9, "modul": 10, "merg": 10, "python3": [10, 13, 20], "skeleton": 10, "structur": 10, "keep": 10, "techniqu": 10, "sync": 10, "between": 10, "rebas": 10, "fals": 10, "com": [10, 13, 15, 20], "diamondlightsourc": 10, "conflict": 10, "area": 10, "setup": [10, 13], "detail": 10, "split": [11, 15, 18], "four": [11, 16, 18], "categori": [11, 18], "access": [11, 18], "side": [11, 18], "bar": [11, 18], "contribut": [11, 15], "doc": [11, 12, 13], "sphinx": [11, 12, 13], "pytest": [11, 13], "analysi": [11, 12, 13], "mypi": [11, 12, 13], "lint": [11, 12, 13], "pre": [11, 12, 13, 17], "tool": [11, 12, 15], "pin": 11, "practic": [11, 18], "step": [11, 13, 18], "dai": 11, "dev": [11, 13], "task": 11, "architectur": 11, "decis": 11, "record": 11, "why": [11, 18], "technic": [11, 16, 18], "materi": [11, 18], "conform": 12, "format": 12, "style": 12, "import": [12, 15], "order": [12, 16], "how": [12, 16], "guid": [12, 15, 16], "napoleon": 12, "extens": 12, "As": 12, "googl": 12, "consid": 12, "hint": 12, "signatur": 12, "def": 12, "func": 12, "arg1": 12, "str": [12, 19], "arg2": 12, "int": 12, "bool": 12, "summari": 12, "extend": 12, "descript": 12, "arg": 12, "return": 12, "valu": 12, "true": 12, "extract": 12, "underlin": 12, "convent": 12, "headl": 12, "head": 12, "2": [12, 15], "These": 13, "instruct": 13, "minim": 13, "first": 13, "either": 13, "host": 13, "machin": 13, "venv": [13, 20], "later": [13, 20], "vscode": 13, "virtualenv": 13, "m": [13, 15, 20], "bin": [13, 20], "activ": [13, 20], "devcontain": 13, "reopen": 13, "prompt": 13, "termin": [13, 20], "graph": 13, "tree": 13, "pipdeptre": 13, "now": [13, 20], "parallel": 13, "my": 15, "own": 15, "home": 15, "monitor": 15, "app": 15, "io": [15, 17], "__version__": [15, 19], "print": 15, "f": 15, "hello": 15, "put": 15, "section": 15, "user": 15, "grand": 16, "unifi": 16, "theori": 16, "david": 16, "la": 16, "secret": 16, "understood": 16, "write": 16, "softwar": [16, 20], "isn": 16, "thing": 16, "thei": 16, "tutori": 16, "refer": [16, 19], "explan": 16, "repres": 16, "purpos": 16, "creation": 16, "understand": 16, "implic": 16, "often": 16, "immens": 16, "topic": 16, "its": [17, 20], "alreadi": 17, "registri": 17, "ghcr": 17, "typic": 18, "usag": 18, "start": 18, "experienc": 18, "about": 18, "intern": 19, "calcul": 19, "pypa": 19, "setuptools_scm": 19, "recommend": 20, "interfer": 20, "path": 20, "featur": 20, "interfac": 20}, "objects": {"": [[19, 0, 0, "-", "domomet"]], "domomet.domomet": [[19, 1, 1, "", "__version__"]]}, "objtypes": {"0": "py:module", "1": "py:data"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "data", "Python data"]}, "titleterms": {"architectur": [0, 1], "decis": [0, 1], "record": [0, 1], "1": 1, "statu": 1, "context": 1, "consequ": 1, "build": [2, 9, 13], "doc": 2, "us": [2, 4, 7, 8], "sphinx": 2, "autobuild": 2, "contribut": 3, "project": 3, "issu": [3, 4], "discuss": 3, "code": [3, 12], "coverag": 3, "develop": [3, 11, 13], "guid": [3, 11, 18], "run": [4, 7, 8, 17], "lint": 4, "pre": 4, "commit": 4, "fix": 4, "vscode": 4, "support": 4, "make": 5, "releas": 5, "pin": 6, "requir": 6, "introduct": 6, "find": 6, "lock": 6, "file": 6, "appli": 6, "remov": 6, "depend": [6, 13], "from": 6, "ci": 6, "test": [7, 9, 13], "pytest": 7, "static": 8, "analysi": 8, "mypi": 8, "contain": [9, 17], "local": 9, "updat": 10, "tool": 10, "tutori": [11, 18], "how": [11, 15, 18], "explan": [11, 18], "refer": [11, 18], "standard": 12, "document": [12, 15, 16], "instal": [13, 20], "clone": 13, "repositori": 13, "see": 13, "what": 13, "wa": 13, "api": [14, 19], "index": 14, "domomet": [15, 19], "i": 15, "structur": 15, "about": 16, "start": 17, "user": 18, "check": 20, "your": 20, "version": 20, "python": 20, "creat": 20, "virtual": 20, "environ": 20, "librari": 20}, "envversion": {"sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx.ext.viewcode": 1, "sphinx": 60}, "alltitles": {"Architectural Decision Records": [[0, "architectural-decision-records"]], "1. Record architecture decisions": [[1, "record-architecture-decisions"]], "Status": [[1, "status"]], "Context": [[1, "context"]], "Decision": [[1, "decision"]], "Consequences": [[1, "consequences"]], "Build the docs using sphinx": [[2, "build-the-docs-using-sphinx"]], "Autobuild": [[2, "autobuild"]], "Contributing to the project": [[3, "contributing-to-the-project"]], "Issue or Discussion?": [[3, "issue-or-discussion"]], "Code coverage": [[3, "code-coverage"]], "Developer guide": [[3, "developer-guide"]], "Run linting using pre-commit": [[4, "run-linting-using-pre-commit"]], "Running pre-commit": [[4, "running-pre-commit"]], "Fixing issues": [[4, "fixing-issues"]], "VSCode support": [[4, "vscode-support"]], "Make a release": [[5, "make-a-release"]], "Pinning Requirements": [[6, "pinning-requirements"]], "Introduction": [[6, "introduction"]], "Finding the lock files": [[6, "finding-the-lock-files"]], "Applying the lock file": [[6, "applying-the-lock-file"]], "Removing dependency locking from CI": [[6, "removing-dependency-locking-from-ci"]], "Run the tests using pytest": [[7, "run-the-tests-using-pytest"]], "Run static analysis using mypy": [[8, "run-static-analysis-using-mypy"]], "Container Local Build and Test": [[9, "container-local-build-and-test"]], "Update the tools": [[10, "update-the-tools"]], "Developer Guide": [[11, "developer-guide"]], "Tutorials": [[11, null], [18, null]], "How-to Guides": [[11, null], [18, null]], "Explanations": [[11, null], [18, null]], "Reference": [[11, null], [18, null]], "Standards": [[12, "standards"]], "Code Standards": [[12, "code-standards"]], "Documentation Standards": [[12, "documentation-standards"]], "Developer install": [[13, "developer-install"]], "Clone the repository": [[13, "clone-the-repository"]], "Install dependencies": [[13, "install-dependencies"]], "See what was installed": [[13, "see-what-was-installed"]], "Build and test": [[13, "build-and-test"]], "API Index": [[14, "api-index"]], "domomet": [[15, "domomet"], [19, "domomet"]], "How the documentation is structured": [[15, "how-the-documentation-is-structured"]], "About the documentation": [[16, "about-the-documentation"]], "Run in a container": [[17, "run-in-a-container"]], "Starting the container": [[17, "starting-the-container"]], "User Guide": [[18, "user-guide"]], "API": [[19, "module-domomet"]], "Installation": [[20, "installation"]], "Check your version of python": [[20, "check-your-version-of-python"]], "Create a virtual environment": [[20, "create-a-virtual-environment"]], "Installing the library": [[20, "installing-the-library"]]}, "indexentries": {"domomet": [[19, "module-domomet"]], "domomet.__version__ (in module domomet)": [[19, "domomet.domomet.__version__"]], "module": [[19, "module-domomet"]]}})