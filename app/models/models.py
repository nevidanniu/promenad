from flask_login import UserMixin
from flask import current_app as app
from app import login, ldap, users
import json


class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn


@login.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


@ldap.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user


class Service:
    def __init__(self, service_id, address, port, tags=None, meta=None, name=None):
        self.service_id = service_id
        self.name = name if name is not None else service_id
        self.address = address
        self.port = int(port)
        self.tags = tags
        self.meta = meta

    @classmethod
    def list_services(cls):
        return app.consul_client.agent.services()

    @classmethod
    def get_service(cls, service_id):
        if service_id in app.consul_client.agent.services():
            service = app.consul_client.agent.services()[service_id]
            return cls(service_id=service['ID'],
                       name=service['Service'],
                       address=service['Address'],
                       port=service['Port'],
                       tags=service['Tags'],
                       meta=service['Meta'])
        else:
            return None

    def set_service(self):
        app.consul_client.agent.service.register(service_id=self.service_id,
                                                 name=self.name,
                                                 address=self.address,
                                                 port=self.port,
                                                 tags=self.tags,
                                                 meta=self.meta)
        return True

    def delete_service(self):
        app.consul_client.agent.service.deregister(service_id=self.service_id)

    @classmethod
    def delete_all(cls):
        services = cls.list_services()
        for service in services:
            app.consul_client.agent.service.deregister(service_id=service)
        return True


class ScanRange:
    def __init__(self, subnet, name=None, exporters: list = None):
        self.root_folder = 'scan_ranges'
        self.subnet = subnet
        self.exporters = exporters
        self.name = name if name is not None else subnet

    @classmethod
    def list_scanranges(cls):
        scan_ranges = list()
        try:
            """try here for situation when root folder doesnt exist"""
            for scan_range in app.consul_client.kv. \
                    get(cls("127.0.0.1/32").root_folder + "/", keys=True, separator='/')[-1]:
                scan_range = scan_range.split('/')[1].replace('_', '/')
                if len(scan_range) > 0:
                    scan_ranges.append(cls.get_scanrange(scan_range))
        except:
            pass
        return scan_ranges

    @classmethod
    def get_scanrange(cls, subnet):
        scan_range = cls(subnet)
        subnet = subnet.replace('/', '_')
        scan_range.subnet = app.consul_client.kv. \
            get(scan_range.root_folder + "/" + subnet + "/", keys=True, separator='/')[-1][0]. \
            split('/')[1].replace('_', '/')
        scan_range.exporters = [r.split('/')[-1] for r in app.consul_client.kv.
            get(scan_range.root_folder + "/" + subnet + "/exporters/", keys=True, separator='/')[-1]
                                if len(r.split('/')[-1]) > 0]
        scan_range.name = app.consul_client.kv. \
            get(scan_range.root_folder + "/" + subnet + "/name", separator='/')[-1]['Value'].decode('utf-8')
        return scan_range

    def set_scanrange(self):
        subnet = self.subnet.replace('/', '_')
        app.consul_client.kv.put(self.root_folder + "/" + subnet + "/", None)
        app.consul_client.kv.put(self.root_folder + "/" + subnet + "/exporters/", None)
        app.consul_client.kv.put(self.root_folder + "/" + subnet + "/name", str(self.name))
        if self.exporters is not None and len(self.exporters) > 0:
            for exporter in self.exporters:
                app.consul_client.kv.put(self.root_folder + "/" + subnet + "/exporters/" + exporter, 'True')
        return True

    def delete_scanrange(self):
        subnet = self.subnet.replace('/', '_')
        return app.consul_client.kv.delete(self.root_folder + "/" + subnet + "/", recurse=True)

    def add_exporter(self, exporter: str):
        subnet = self.subnet.replace('/', '_')
        return app.consul_client.kv.put(self.root_folder + "/" + subnet + "/exporters/" + exporter, 'True')

    def delete_exporter(self, exporter: str):
        subnet = self.subnet.replace('/', '_')
        return app.consul_client.kv.delete(self.root_folder + "/" + subnet + "/exporters/" + exporter, 'True')


class Exporter:
    def __init__(self, name: str, port: str = "", meta: dict = dict(), tags: list = list()):
        self.root_folder = 'exporters'
        self.name = name
        self.port = port
        self.meta = meta
        self.tags = tags

    @classmethod
    def get_exporter(cls, name):
        exporter = cls(name)
        exporter.port = app.consul_client.kv. \
            get(exporter.root_folder + "/" + exporter.name + "/port", separator='/')[-1]['Value'].decode('utf-8')
        exporter.meta = json.loads(app.consul_client.kv.
                                   get(exporter.root_folder + "/" + exporter.name + "/meta", separator='/')[-1][
                                       'Value'])
        exporter.tags = json.loads(app.consul_client.kv.
                                   get(exporter.root_folder + "/" + exporter.name + "/tags", separator='/')[-1][
                                       'Value'])
        return exporter

    def set_exporter(self):
        app.consul_client.kv.put(self.root_folder + "/" + self.name + "/", None)
        app.consul_client.kv.put(self.root_folder + "/" + self.name + "/port", self.port)
        app.consul_client.kv.put(self.root_folder + "/" + self.name + "/meta", json.dumps(self.meta))
        app.consul_client.kv.put(self.root_folder + "/" + self.name + "/tags", json.dumps(self.tags))
        return True

    def delete_exporter(self):
        for scan_range in ScanRange.list_scanranges():
            scan_range.delete_exporter(self.name)
        return app.consul_client.kv.delete(self.root_folder + "/" + self.name + "/", 'True')

    @classmethod
    def list_exporters(cls):
        exporters = list()
        try:
            """try here for situation when root folder doesnt exist"""
            for exporter in app.consul_client.kv. \
                    get(cls("generic_exporter", '0').root_folder + "/", keys=True, separator='/')[-1]:
                exporter = exporter.split('/')[1]
                if len(exporter) > 0:
                    exporters.append(cls.get_exporter(name=exporter))
        except:
            pass
        return exporters
