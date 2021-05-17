import os
from base64 import urlsafe_b64encode
from os import urandom

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_babel import get_locale

from web.forms import SubscriptionForm

blueprint = Blueprint("public", __name__)


def discord_auth_uri_with_state(state):
    base_uri = "https://discord.com/api/oauth2/authorize"
    redirect_uri = url_for('auth.webhook', _external=True)
    client_id = os.getenv('DISCORD_CLIENT_ID')
    return "{}?response_type=code&client_id={}&scope=webhook.incoming&redirect_uri={}&state={}".format(
        base_uri, client_id, redirect_uri, state
    )


@blueprint.route("/")
def root():
    """Home page"""
    locale = get_locale()
    return redirect(url_for('public.subscribe', locale=str(locale)))


@blueprint.route("/<locale>", methods=('GET', 'POST'))  # type: ignore
def subscribe(locale):
    form = SubscriptionForm()

    if request.method == 'GET':
        return render_template("index.html", form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            session['entry_uri'] = request.path

            state = urlsafe_b64encode(urandom(12)).decode('utf-8')
            session['state'] = state
            discord_auth_uri = discord_auth_uri_with_state(state)

            session['webhook_setting'] = {
                'is_nsfw': form.is_nsfw.data,
                'lang': form.language.data
            }

            return redirect(discord_auth_uri)

        flash("wtf are you doing?")
        return render_template("index.html", form=form, error="WTF?")
