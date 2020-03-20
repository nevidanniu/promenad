import wtforms
from wtforms import validators, widgets
from flask_wtf import FlaskForm


class NewSubnetsForm(FlaskForm):
    newsubnet = wtforms.StringField(label="Subnet",
                                    validators=[validators.regexp('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(3[0-2]|[01]?[1-2][0-9])',
                                                                  message='Must be valid subnet in CIDR notation')])
    newsubnet_name = wtforms.StringField(label='Subnet name')
    submit = wtforms.SubmitField('Add subnet')


class ExporterMultipleCheckBoxForm(wtforms.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SubnetExporterForm(FlaskForm):
    exporters = ExporterMultipleCheckBoxForm('Exporters')
    name = wtforms.StringField(label='Subnet name')
    submit = wtforms.SubmitField('Save changes')
