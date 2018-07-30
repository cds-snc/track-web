from http import HTTPStatus
import os

from flask import render_template, Response, abort, request, redirect
import ujson

from track.data import FIELD_MAPPING
from track import models
from track.cache import cache


def register(app):

    # Default route checks accept-language header
    # Redirects based on browser language, defaults to english
    @app.route("/")
    def index():
        user_lang = request.headers.get("Accept-Language", "en")
        if user_lang[:2] == "fr":
            return redirect("/fr/index/")
        else:
            return redirect("/en/index/")

    @app.route("/ping")
    def health_check():
        return "PONG"

    @app.route("/en/")
    @app.route("/fr/")
    @app.route("/en/index/")
    @app.route("/fr/index/")
    def splash_page():
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, "index"))

    @app.route("/en/organizations/")
    @app.route("/fr/organisations/")
    def organizations():
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, "organizations"))

    @app.route("/en/domains/")
    @app.route("/fr/domaines/")
    def https_domains():
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, "domains"))

    @app.route("/en/guidance/")
    @app.route("/fr/directives/")
    def guidance():
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, "guidance"))

    @app.route("/en/help/")
    @app.route("/fr/aide/")
    def help():
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, "help"))

    def generate_path(prefix, page_id):
        if prefix == "en" or prefix == "fr":
            return os.path.join(prefix, "{}.html".format(page_id))
        else:
            abort(HTTPStatus.NOT_FOUND)

    @app.route("/cache-buster")
    def cache_bust():
        try:
            cache.clear()
            return "", HTTPStatus.NO_CONTENT
        except Exception as exc:
            return str(exc), HTTPStatus.INTERNAL_SERVER_ERROR

    ##
    # Data endpoints.

    # High-level %'s, used to power the donuts.
    @app.route("/data/reports/<report_name>.json")
    @cache.cached()
    def report(report_name):
        report_name = "https" if report_name == "compliance" else report_name

        response = Response(ujson.dumps(models.Report.latest().get(report_name, {})))
        response.headers["Content-Type"] = "application/json"
        return response

    # Detailed data per-parent-domain.
    @app.route("/data/domains/<report_name>.json")
    @cache.cached()
    def domain_report(report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible_parents(report_name)
        domains = sorted(domains, key=lambda k: k["domain"])

        response = Response(ujson.dumps({"data": domains}))
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route("/data/domains/<language>/<report_name>.csv")
    @cache.cached()
    def domain_report_csv(report_name, language):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible_parents(report_name)
        domains = sorted(domains, key=lambda k: k["domain"])

        response = Response(models.Domain.to_csv(domains, report_name, language))
        response.headers["Content-Type"] = "text/csv"

    @app.route("/data/domains-table.json")
    @cache.cached()
    def domains_table():
        domains = models.Domain.find_all(
            {"https.eligible_zone": True, "is_parent": True},
            {
                "_id": False,
                "domain": True,
                "organization_name_en": True,
                "organization_name_fr": True,
                "is_parent": True,
                "base_domain": True,
                "https.bod_crypto": True,
                "https.eligible": True,
                "https.enforces": True,
                "https.hsts": True,
                "https.compliant": True,
                "https.bod_crypto": True,
                "https.good_cert": True,
                "totals.https.enforces": True,
                "totals.https.hsts": True,
                "totals.https.compliant": True,
                "totals.https.eligible": True,
                "totals.crypto.bod_crypto": True,
                "totals.crypto.good_cert": True,
                "totals.crypto.eligible": True,
            },
        )
        response = Response(ujson.dumps({"data": domains}))
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route("/data/organizations-table.json")
    @cache.cached()
    def organizations_table():
        organizations = models.Organization.find_all(
            {"https.eligible": {"$gt": 0}},
            {
                "_id": False,
                "total_domains": True,
                "name_en": True,
                "name_fr": True,
                "https.compliant": True,
                "https.enforces": True,
                "https.hsts": True,
                "https.eligible": True,
                "crypto.bod_crypto": True,
                "crypto.good_cert": True,
                "crypto.eligible": True,
            },
        )
        # app.logger.debug([o for o in organizations])
        response = Response(ujson.dumps({"data": organizations}))
        response.headers["Content-Type"] = "application/json"
        return response

    # Detailed data per-host for a given report.
    @app.route("/data/hosts/<report_name>.json")
    @cache.cached()
    def hostname_report(report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible(report_name)

        # sort by base domain, but subdomain within them
        domains = sorted(domains, key=lambda k: k["domain"])
        domains = sorted(domains, key=lambda k: k["base_domain"])

        response = Response(ujson.dumps({"data": domains}))
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route("/data/hosts/<language>/<report_name>.csv")
    @cache.cached()
    def hostname_report_csv(language, report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible(report_name)

        # sort by base domain, but subdomain within them
        domains = sorted(domains, key=lambda k: k["domain"])
        domains = sorted(domains, key=lambda k: k["base_domain"])

        response = Response(models.Domain.to_csv(domains, report_name, language))
        response.headers["Content-Type"] = "text/csv"
        return response

    # Detailed data for all subdomains of a given parent domain, for a given report.
    @app.route("/data/hosts/<domain>/<report_name>.json")
    @cache.cached()
    def hostname_report_for_domain(domain, report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible_for_domain(domain, report_name)

        # sort by hostname, but put the parent at the top if it exist
        domains = sorted(domains, key=lambda k: k["domain"])
        domains = sorted(domains, key=lambda k: k["is_parent"], reverse=True)

        response = Response(ujson.dumps({"data": domains}))
        response.headers["Content-Type"] = "application/json"
        return response

    # Detailed data for all subdomains of a given parent domain, for a given report.
    @app.route("/data/hosts/<domain>/<language>/<report_name>.csv")
    @cache.cached()
    def hostname_report_for_domain_csv(domain, language, report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Domain.eligible_for_domain(domain, report_name)

        # sort by hostname, but put the parent at the top if it exist
        domains = sorted(domains, key=lambda k: k["domain"])
        domains = sorted(domains, key=lambda k: k["is_parent"], reverse=True)

        response = Response(models.Domain.to_csv(domains, report_name, language))
        response.headers["Content-Type"] = "text/csv"
        return response

    @app.route("/data/organizations/<report_name>.json")
    @cache.cached()
    def organization_report(report_name):
        report_name = "https" if report_name == "compliance" else report_name

        domains = models.Organization.eligible(report_name)
        response = Response(ujson.dumps({"data": domains}))
        response.headers["Content-Type"] = "application/json"
        return response

    # Every response back to the browser will include these web response headers
    @app.after_request
    def apply_headers(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = 1
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), HTTPStatus.NOT_FOUND

    @app.errorhandler(models.QueryError)
    def handle_invalid_usage(error):
        app.logger.error(error)
        return render_template("404.html"), HTTPStatus.NOT_FOUND

    @app.before_request
    def verify_cache():
        if not models.Flag.get_cache():
            app.logger.info('Clearing cache...')
            cache.clear()
            models.Flag.set_cache(True)
