from sanic import Blueprint
from sanic import response

from hexi.service import web
from hexi.util import taillog

bp = Blueprint('log', url_prefix='/core/log')


@bp.route('/api/logs')
async def get_logs(request):
  return response.json({ 'code': 200, 'data': taillog.log_queue })


def init():
  web.app.blueprint(bp)
