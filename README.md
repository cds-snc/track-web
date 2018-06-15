CircleCI Status: [![CircleCI](https://circleci.com/gh/cds-snc/track-web.svg?style=svg)](https://circleci.com/gh/cds-snc/track-web)

## Track Government of Canada domains's adherance to digital security practices

How the GC domain space is doing at best practices and federal requirements.

| Documentation                                           |
| ------------------------------------------------------- |
| [Development Setup Instructions](#development-setup)    |
| [Local Deploy Step-by-step](docs/local-instructions.md) |
| [Deployment Docs](docs/deploy.md)                       |

## Developer Notes

This repository is using [snyk](https://snyk.io/org/cds-snc) to scan our dependencies for vulnerabilities.  
Unfortunatly Synk lacks the ability to detect the dependencies listed in the `setup.py` file.
To get around this we are have the dependencies synced between the `setup.py` and `requirements.txt` (which snyk can scan) files.  
If you are developing this and add an aditional dependency, make sure to add it to both locations

## Development Setup

For development purposes it is recommended that you install [mongodb](https://www.mongodb.com/) and run the database locally.

This dashboard is a [Flask](http://flask.pocoo.org/) app written for **Python 3.5 and up**. We recommend [pyenv](https://github.com/yyuu/pyenv) for easy Python version management.

To setup local python dependencies you can run `make setup` from the root of the repository. We recommend that this is done from within a virtual environment

To prepare data for presentation, please see the [tracker](https://github.com/cds-snc/tracker) repository.

* Install dependencies:

```bash
pip install -r requirements.txt
```

* If developing this dashboard app, you will also need the development requirements
```bash
pip install .[development]
```

* If developing the stylesheets, you will also need [Sass](http://sass-lang.com/), [Bourbon](http://bourbon.io/), [Neat](http://neat.bourbon.io/), and [Bitters](http://bitters.bourbon.io/).

```bash
gem install sass bourbon neat bitters
```

* If editing styles during development, keep the Sass auto-compiling with:

```bash
make watch
```

* And to run the app in development, use:

```bash
make debug
```

This will run the app with `DEBUG` mode on, showing full error messages in-browser when they occur.

When running in development mode it is expected that you have a database running locally, accessable via `localhost:27017`.

To produce some data for the flask app to display, follow the instructions in the following section.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

### Origin 

This project was originally forked from [18F](https://github.com/18f/pulse) and has been modified to fit the Canadian context.
