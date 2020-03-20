import wtforms
from wtforms import validators
from flask_ldap3_login.forms import LDAPLoginForm


class LoginForm(LDAPLoginForm):
    username = wtforms.StringField('Username', validators=[validators.Required()],
                                   render_kw={"placeholder": "LDAP username", "autofocus": "true"})
    password = wtforms.PasswordField('Password', validators=[validators.Required()],
                                     render_kw={"placeholder": "LDAP password"})
    submit = wtforms.SubmitField('Submit')
    remember_me = wtforms.HiddenField('Remember Me', default=True)

