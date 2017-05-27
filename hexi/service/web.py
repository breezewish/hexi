import asyncio
import logging

from sanic import Sanic
from sanic import Blueprint
from hexi.service import event

_logger = logging.getLogger(__name__)

app = Sanic()


app.static('/', 'hexi/ui/root/index.html')

routeCore = Blueprint('core', url_prefix='/core')
routeCore.static('/static', 'hexi/.ui_built')
app.blueprint(routeCore)


def init():
  server = app.create_server(host='0.0.0.0', port=8000, log_config=None)
  asyncio.ensure_future(server)
