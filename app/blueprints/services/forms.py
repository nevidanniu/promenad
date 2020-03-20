import wtforms
from wtforms import validators
from flask_wtf import FlaskForm


class ServiceEditForm(FlaskForm):
    service_name = wtforms.StringField(label="Service name")
    service_meta = wtforms.TextAreaField(label="Meta", render_kw={'class': 'form-control', 'rows': 8})
    service_tag = wtforms.StringField(label="Tags")
    submit = wtforms.SubmitField('Save changes')
