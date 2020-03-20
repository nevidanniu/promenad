from flask import render_template, redirect, url_for, request, flash
from app.blueprints.exporters import bp
from app.models.models import Exporter
from .forms import ExporterForm, ExporterEditForm
from flask_login import login_required
import re


@bp.route('/', methods=['GET', 'POST'])
@login_required
def exporters():
    form = ExporterForm()
    exporters = Exporter.list_exporters()
    if form.validate_on_submit():
        Exporter(form.exporter_name.data, str(form.exporter_port.data)).set_exporter()
        flash('New exporter added: {} '.format(form.exporter_name.data), 'message')
        return redirect(url_for('exporters.exporters'))
    return render_template('exporters.html', form=form, exporters=exporters)


@bp.route('/delete', methods=['GET'])
@login_required
def exporter_delete():
    exporter = request.args.get("exporter")
    Exporter(exporter).delete_exporter()
    flash('Exporter removed: {} '.format(exporter), 'message')
    return redirect(url_for('exporters.exporters'))


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def exporter_edit():
    exporter = request.args.get("exporter")
    exporter = Exporter.get_exporter(exporter)
    form = ExporterEditForm()
    if form.validate_on_submit():
        exporter_meta = list()
        for line in form.exporter_meta.data.split("\r\n"):
            if ':' in line:
                exporter_meta.append(line)
        exporter.meta = dict(map(lambda s: s.split(':'), exporter_meta)) or dict()
        form.exporter_tag.data = re.sub(r"[;?:?|]", ",", form.exporter_tag.data)
        exporter.tags = form.exporter_tag.data.split(",") or list()
        exporter.port = str(form.exporter_port.data)
        exporter.set_exporter()
        flash('Changes saved', 'message')
        return redirect(url_for('exporters.exporters'))
    else:
        form.exporter_meta.data = '\r\n'.join([k+":"+exporter.meta[k] for k in exporter.meta])
        form.exporter_tag.data = ','.join(exporter.tags)
        form.exporter_port.data = exporter.port
    return render_template('exporter_edit.html', form=form, exporter=exporter)


