## Making Additions

This document is meant to give an explanation of the location of various components of the system, and how one would change or add to them.

The dashboard is a [Flask](http://flask.pocoo.org/) application, meaning that it uses python for page routing, data retrieval, and to render [Jinja2](http://jinja.pocoo.org/docs/latest/) templates into html that is then served to the user. The resulting HTML pages use javascript to request and display the data and handle interactions with the pages.

### Frontend Content

The frontend content is located within the `track` subdirectory, in the `templates` and `static` directoriies.
* `static` - for static content such as javascript, css, images, etc.
* `templates` - for the Jinja2 templates

If you need to make an addition or edit to the frontend content, it will likely be isolated to one or both of these folders.  
To make an edit to the copy, simply find where it is in the `templates` directory, and make the edit (remembering to do so in both languages).
To make an edit to the page behavior or style, it is likely that an edit will need to be made to some of the static files.

#### CSS

This project includes a precompiled [Tailwind](https://tailwindcss.com/docs/what-is-tailwind/) css file. Tailwind is a utility-first CSS framework for rapidly building custom user interfaces. 
Any utility classes listed in their documentation can be used in this project, and you will see them throughout the markup. For example, a link definition may look like this:

```<a tabindex="-1" class="text-xl text-https-blue no-underline hover:underline" href="/en/guidance/">```

### Routing, page rending, and data retrieval

To make a change to the backend of the dashboard, the `.py` files in `track` contain what you need.  
* `__init__.py` - function for creating and initializing the flask application
* `data.py` - mappings from database document property names to human readable names for the CSV export and frontend.
* `helpers.py` - small number of helper functions for the template rendering.
* `models.py` - abstraction layer on top of the database. Application makes calls into this module to interact with the database.
* `views.py` - route definitions. Code that will be executing when users attempt to visit paths (such as `/en/domains/`, which displays the English domains page).
* `wsgi.py` - simple module that just creates and holds a reference to the flask app.
