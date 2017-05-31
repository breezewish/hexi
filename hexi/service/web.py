import asyncio
import logging

from sanic import Sanic
from sanic import Blueprint
from hexi.service import event

_logger = logging.getLogger(__name__)

app = Sanic()


app.static('/', 'hexi/ui/root/index.html')

bp = Blueprint('core', url_prefix='/core')
bp.static('/static', 'hexi/.ui_built')
app.blueprint(bp)


async def on_start(e):
  server = app.create_server(host='0.0.0.0', port=8000, log_config=None)
  asyncio.ensure_future(server)


def init():
  event.subscribe(on_start, ['hexi.start'])
