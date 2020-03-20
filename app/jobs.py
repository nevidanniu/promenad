from app import *
from flask import url_for
from app.models.models import ScanRange
import urllib3

app = create_app(Config)


@scheduler.task('interval', id='scan_subnets', seconds=Config.PROMENAD_SCAN_INTERVAL)
def scan_subnets():
    with app.app_context():
        scan_ranges = ScanRange.list_scanranges()
        http = urllib3.PoolManager()
        for scan_range in scan_ranges:
            http.request('GET', Config.PROMENAD_SCAN_ENDPOINT+"?rest=1&subnet="+scan_range.subnet)
