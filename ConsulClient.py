import consul


class ConsulClient():
    def __init__(self):
        self.consul = None

    def init_app(self, app):
        self.consul = consul.Consul(host=app.config['CONSUL_HOST'],
                                    port=app.config['CONSUL_PORT'],
                                    scheme=app.config['CONSUL_SCHEME'],
                                    verify=app.config['CONSUL_VERIFY'],
                                    cert=app.config['CONSUL_CERT'])
        app.consul_client = self.consul
        self.app = app