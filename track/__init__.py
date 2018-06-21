from flask import Flask
from flask_compress import Compress

def create_app(environment='development'):
    app = Flask(__name__, instance_relative_config=True)

    # Gzip compress most things
    app.config['COMPRESS_MIMETYPES'] = [
        'text/html', 'text/css', 'text/xml',
        'text/csv', 'application/json', 'application/javascript'
    ]
    if environment == 'development':
        app.config.from_object('track.config.DevelopmentConfig')
    elif environment == 'testing':
        app.config.from_object('track.config.TestingConfig')
    else:
        app.config.from_object('track.config.ProductionConfig')
    app.config.from_pyfile('application.cfg', silent=True)

    import logging
    import logging.handlers
    handler = logging.handlers.SysLogHandler(address=app.config.get('SYSLOG_ADDRESS'))
    handler.setLevel(app.config.get('LOGLEVEL'))

    formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    Compress(app)

    from track.cache import cache
    cache.init_app(app)

    from track import views
    views.register(app)

    from track import helpers
    helpers.register(app)

    from track.models import db
    db.init_app(app)

    return app
