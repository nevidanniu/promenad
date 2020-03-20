from flask import render_template, current_app as app, redirect, url_for, request, flash
from flask_login import login_required
from app.blueprints.main import bp


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('services.services'))

@bp.route('/test_flash')
def test_flash():
    message = "default message"
    flash(message, 'warning')
    return render_template('index.html')

