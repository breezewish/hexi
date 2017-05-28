from sanic import Blueprint
from sanic.response import json

from hexi.service import web
from hexi.util import taillog

bp = Blueprint('log', url_prefix='/core/log')


@bp.route('/api/logs')
async def webGetLogs(request):
  return json(taillog.log_queue)


def init():
  web.app.blueprint(bp)
