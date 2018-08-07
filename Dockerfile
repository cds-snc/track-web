MAINTAINER David Buckley <david.buckley@cds-snc.ca>
LABEL Description="Track Web Security Compliance" Vendor="Canadian Digital Service"

FROM python:3.5 as python-base
COPY requirements.txt /opt/track-web/requirements.txt
COPY setup.py /opt/track-web/setup.py 
COPY track /opt/track-web/track
COPY MANIFEST.in /opt/track-web/MANIFEST.in

# Build wheels to install into production image
# Force a build with --no-binary to get around the case where a wheel is available for python:3.5 but not python:3.5-alpine
RUN pip install --upgrade pip && mkdir wheels && pip wheel --no-binary :all: -r /opt/track-web/requirements.txt -w wheels && pip wheel --no-deps /opt/track-web/ -w wheels

FROM python:3.5-alpine
MAINTAINER David Buckley <david.buckley@cds-snc.ca>
LABEL Description="Track Digital Security Compliance" Vendor="Canadian Digital Service"
 
COPY --from=python-base /wheels /wheels
 
RUN pip install /wheels/* && rm -rf /wheels /root/.cache/pip && \
    addgroup -S track-web && adduser -S -G track-web track-web && \
    mkdir -p /opt/track-web/.cache && \
    chown -R track-web /opt/track-web
USER track-web:track-web
 
EXPOSE 5000
ENTRYPOINT ["gunicorn", "track.wsgi:app", "--bind=0.0.0.0:5000", "--worker-class=gthread", "--access-logfile=-", "--error-logfile=-", "--capture-output"]
