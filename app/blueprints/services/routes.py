from flask import render_template, redirect, url_for, request, flash
from app.blueprints.services import bp
from app.models.models import Service, ScanRange, Exporter
from flask_login import login_required
from functools import partial
from .forms import ServiceEditForm
import socket
import re
from netaddr import *
from app import executor


@bp.route('/', methods=['GET'])
@login_required
def services():
    services = Service.list_services()
    return render_template('services.html', services=services)


@bp.route('/skipped', methods=['GET'])
@login_required
def skipped_services():
    services = Service.list_services()
    return render_template('skipped_services.html', services=services)

@bp.route('/skip', methods=['GET'])
@login_required
def service_skip():
    service_id = request.args.get("service")
    skip = request.args.get("skip") == "True" or request.args.get("skip") == "true"
    urlback = request.args.get("urlback") or url_for('services.services')
    service = Service.get_service(service_id)
    if skip:
        service.meta['skip'] = 'true'
    else:
        del service.meta['skip']
    service.set_service()
    flash('Changes saved', 'message')
    return redirect(urlback)

@bp.route('/delete', methods=['GET'])
@login_required
def service_delete():
    service = request.args.get("service")
    Service.get_service(service).delete_service()
    flash('Service removed: {}'.format(service), 'message')
    return redirect(url_for('services.services'))


@bp.route('/delete_all', methods=['GET'])
@login_required
def service_delete_all():
    Service.delete_all()
    flash('Services removed', 'message')
    return redirect(url_for('services.services'))


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def service_edit():
    service_id = request.args.get("service")
    service = Service.get_service(service_id)
    form = ServiceEditForm()
    if form.validate_on_submit():
        service.name = form.service_name.data
        service_meta = list()
        for line in form.service_meta.data.split("\r\n"):
            if ':' in line:
                service_meta.append(line)
        service.meta = dict(map(lambda s: s.split(':'), service_meta)) or dict()
        form.service_tag.data = re.sub(r"[;?:?|]", ",", form.service_tag.data)
        service.tags = form.service_tag.data.split(",") or list()
        service.set_service()
        flash('Changes saved', 'message')
        return redirect(url_for('services.services'))
    else:
        form.service_name.data = service.name
        form.service_meta.data = '\r\n'.join([k+":"+service.meta[k] for k in service.meta])
        form.service_tag.data = ','.join(service.tags)
        return render_template('service_edit.html', form=form, service=service)


@bp.route('/scan', methods=['GET'])
# @login_required
def service_scan():
    subnet = request.args.get("subnet")
    rest = bool(request.args.get('rest'))
    scan_range = ScanRange.get_scanrange(subnet)
    exporters = list()
    for exporter in scan_range.exporters:
        exporters.append(Exporter.get_exporter(exporter))
    ip_network = IPNetwork(subnet)
    for exporter in exporters:
        additional_meta = {
            'subnet': subnet,
            'subnet_name': scan_range.name,
            'exporter': exporter.name}
        func = partial(process_service, exporter, additional_meta)
        executor.submit(func)
        executor.map(func, ip_network)
        flash('Scan completed: {}'.format(subnet), 'message')
    if rest:
        return '', 200
    return redirect(url_for('subnets.subnets'))


def process_service(exporter, additional_meta, ip):
    try:
        service_ip = ip.ipv4().format()
        if check_port_open(service_ip, int(exporter.port)):
            if not Service.get_service(service_ip+":"+str(int(exporter.port))):
                exporter.meta.update(additional_meta)
                Service(service_id=service_ip+":"+str(int(exporter.port)),
                        address=service_ip,
                        port=int(exporter.port),
                        tags=exporter.tags,
                        meta=exporter.meta).set_service()
    except Exception as e:
        print(e)


def check_port_open(check_ip, check_port, tcp_timeout=0.1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(float(tcp_timeout))
    result = sock.connect_ex((check_ip, int(check_port)))
    return result == 0
