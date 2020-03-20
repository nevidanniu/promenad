from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.blueprints.subnets import bp
from app.models.models import ScanRange, Exporter
from .forms import NewSubnetsForm, SubnetExporterForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def subnets():
    subnets = ScanRange.list_scanranges()
    form = NewSubnetsForm()
    if form.validate_on_submit():
        subnet = form.newsubnet.data
        subnet_name = form.newsubnet_name.data if form.newsubnet_name.data else None
        ScanRange(subnet, subnet_name).set_scanrange()
        flash('Subnet added: {}'.format(subnet), 'message')
        return redirect(url_for('subnets.subnets'))
    return render_template('scan_ranges.html', subnets=subnets, form=form)


@bp.route('/delete', methods=['GET'])
@login_required
def subnet_delete():
    subnet = request.args.get("subnet")
    ScanRange(subnet).delete_scanrange()
    flash('Subnet removed: {}'.format(subnet), 'message')
    return redirect(url_for('subnets.subnets'))


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def subnet_edit():
    subnet = request.args.get("subnet")
    scan_range = ScanRange.get_scanrange(subnet)
    exporters = [(r.name, r.name) for r in Exporter.list_exporters()]
    exporter_form = SubnetExporterForm()
    exporter_form.exporters.choices = exporters
    if exporter_form.validate_on_submit():
        scan_range.name = exporter_form.name.data
        scan_range.set_scanrange()
        exporters_to_delete = [r for r in scan_range.exporters if r not in exporter_form.exporters.data]
        for exporter in exporters_to_delete:
            scan_range.delete_exporter(exporter)
        exporters_to_add = [r for r in exporter_form.exporters.data if r not in scan_range.exporters]
        for exporter in exporters_to_add:
            scan_range.add_exporter(exporter)
        flash('Changes saved', 'message')
        return redirect(url_for('subnets.subnets'))
    else:
        exporter_form.exporters.data = scan_range.exporters
        exporter_form.name.data = scan_range.name
        return render_template('scan_range_edit.html', scan_range=scan_range, exporter_form=exporter_form)




