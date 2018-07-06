[![CircleCI](https://circleci.com/gh/cds-snc/track-web.svg?style=svg)](https://circleci.com/gh/cds-snc/track-web)
[![Known Vulnerabilities](https://snyk.io/test/github/cds-snc/track-web/badge.svg)](https://snyk.io/test/github/cds-snc/track-web)


## Track Government of Canada domains's adherence to web security practices

This repository is one component of _Track web security compliance_, a web-based application that scans Government of Canada websites and reports how they are meeting good web security practices, as outlined in [Information Technology Policy Implementation Notice (ITPIN): Implementing HTTPS for Secure Web Connections](https://www.canada.ca/en/treasury-board-secretariat/services/information-technology/policy-implementation-notices.html). `track-web` is a web application that displays the results of [tracker](https://github.com/cds-snc/tracker), the domain scanner. This is what it looks like, in English and French, with demo data: 

| English | French |
|---------|--------|
|![English landing page: header with title, some text, and a chart showing number of domains that enforce HTTPS](/docs/img/en-landing.png)  |  ![French landing page: header with title, some text, and a chart showing number of domains that enforce HTTPS](/docs/img/fr-landing.png) |
|![English dashboard page: text, a search bar, and a table with columns: Organization, ITPIN Compliant, Enforces HTTPS, HSTS, Free of known weak protocols and ciphers, Uses approved certificates](/docs/img/en-dashboard.png) | ![French dashboard page: text, a search bar, and a table with columns: Organization, ITPIN Compliant, Enforces HTTPS, HSTS, Free of known weak protocols and ciphers, Uses approved certificates](/docs/img/fr-dashboard.png) |



-------

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

> This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

### Origin 

This project was originally forked from [18F](https://github.com/18f/pulse) and has been modified to fit the Canadian context.
