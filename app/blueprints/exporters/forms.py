import wtforms
from wtforms import validators
from flask_wtf import FlaskForm


class ExporterEditForm(FlaskForm):
    exporter_port = wtforms.IntegerField(label="Port number",
                                         validators=[validators.DataRequired(message='Please enter valid port number')])
    exporter_meta = wtforms.TextAreaField(label="Meta", render_kw={'class': 'form-control', 'rows': 8})
    exporter_tag = wtforms.StringField(label="Tags")
    submit = wtforms.SubmitField('Save changes')

class ExporterForm(FlaskForm):
    exporter_port = wtforms.IntegerField(label="Port number",
                                         validators=[validators.DataRequired(message='Please enter valid port number')])
    exporter_name = wtforms.StringField(label="Exporter name",
                                        validators=[validators.DataRequired(message='Please enter exporter name')])
    submit = wtforms.SubmitField('Add exporter')
