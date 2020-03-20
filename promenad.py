from app import create_app, scheduler
from app.jobs import scan_subnets

app = create_app()


scheduler.init_app(app)
scheduler.start()
