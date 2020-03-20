from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm
from app.blueprints.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """main login func"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(url_for('main.index'))
    elif 'Invalid Username/Password.' in form.username.errors and 'Invalid Username/Password.' in form.password.errors:
        flash('Invalid Username/Password', 'warning')
        form.username.errors.clear()
        form.password.errors.clear()
    return render_template('auth.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
