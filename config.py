import os


class Config(object):
    SECRET_KEY = os.environ.get('AUTH_TOKEN') or 'you-will-never-guess'
    if os.environ.get('SERVER_NAME'):
        SERVER_NAME = os.environ.get('SERVER_NAME')
    TEMPLATES_AUTO_RELOAD = True
    PROMENAD_SCAN_ENDPOINT = os.environ.get('PROMENAD_SCAN_ENDPOINT') or "http://127.0.0.1:8000/services/scan"
    PROMENAD_SCAN_INTERVAL = int(os.environ.get('PROMENAD_SCAN_INTERVAL')) \
        if os.environ.get('PROMENAD_SCAN_INTERVAL') is not None else 600
    LDAP_HOST = os.environ.get('LDAP_HOST') or 'localhost:389'
    LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN') or 'dc=org,dc=ru'
    LDAP_USER_DN = 'ou=Users'
    LDAP_GROUP_DN = 'ou=Groups'
    LDAP_GROUP_OBJECT_FILTER = "(objectclass=groupOfUniqueNames)"
    LDAP_BIND_USER_DN = None
    LDAP_BIND_USER_PASSWORD = None
    LDAP_USER_RDN_ATTR = 'cn'
    LDAP_USER_LOGIN_ATTR = 'uid'
    DEVELOP = os.environ.get('DEVELOP') or False
    SCHEDULER_API_ENABLED = True
    CONSUL_HOST = os.environ.get('CONSUL_HOST') or "consul.monitoring.svc"
    CONSUL_PORT = int(os.environ.get('CONSUL_PORT')) if os.environ.get('CONSUL_PORT') is not None else 8500
    CONSUL_SCHEME = os.environ.get('CONSUL_SCHEME') or "http"
    CONSUL_VERIFY = False
    CONSUL_CERT = None
