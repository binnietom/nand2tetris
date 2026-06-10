# nand2tetris

![PyPI version](https://img.shields.io/pypi/v/nand2tetris.svg)

Python simulation of end to end working computer from first principles.

* [GitHub](https://github.com/Tom Binnie/nand2tetris/) | [PyPI](https://pypi.org/project/nand2tetris/) | [Documentation](https://Tom Binnie.github.io/nand2tetris/)
* Created by [Thomas Binnie](https://audrey.feldroy.com/) | GitHub [@binnietom](https://github.com/binnietom) | PyPI [@binnietom](https://pypi.org/user/binnietom/)
* MIT License

## Features

# nand2tetris

Simulated computer from first principles all in python. Based on "Elements of Computing Systems" Nisan and Schocken.

Architecture is split into 2 layers:

  hardware (Nand -> Logic gates -> ALU, RAM chips -> CPU)  
and
  software (Machine language -> VM Code -> high-level language -> Programmer)

Each level is planned to be an abstraction that relies on parts/objects from the last section.

## Hardware

### Chapter 1 - Boolean Logic

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://Tom Binnie.github.io/nand2tetris/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/nand2tetris.git
cd nand2tetris

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `n2t`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

nand2tetris was created in 2026 by Thomas Binnie.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
