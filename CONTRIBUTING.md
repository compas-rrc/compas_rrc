# Contributor's Guide

Contributions are always welcome and greatly appreciated!

## Code contributions

We love pull requests from everyone! Here's a quick guide to improve the code:

1. Fork [the repository](https://github.com/compas-rrc/compas_rrc) and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `venv`, `conda`, etc).
3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Make sure all tests pass:

   ```bash
   invoke test
   ```

5. Start making your changes to the **main** branch (or branch off of it).
6. Make sure all tests still pass:

   ```bash
   invoke test
   ```

7. Add yourself to `AUTHORS.md`.
8. Commit your changes and push your branch to GitHub.
9. Create a [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
   through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests.
* `invoke`: Show available tasks.

## Documentation improvements

We could always use more documentation, whether as part of the
introduction/examples/usage documentation or API documentation in docstrings.

Documentation is written in Markdown and uses
[MkDocs](https://www.mkdocs.org/) with the
[Material](https://squidfunk.github.io/mkdocs-material/) theme to generate the
HTML output. API reference pages are generated from numpydoc-style docstrings
by [mkdocstrings](https://mkdocstrings.github.io/).

Once you made the documentation changes locally, run the documentation generation:

```bash
invoke docs
```

To preview the site with live reload while you edit:

```bash
mkdocs serve
```

## Bug reports

When [reporting a bug](https://github.com/compas-rrc/compas_rrc/issues)
please include:

* Operating system name and version.
* Python version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests and feedback

The best way to send feedback is to file an issue on
[GitHub](https://github.com/compas-rrc/compas_rrc/issues). If you are proposing
a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
