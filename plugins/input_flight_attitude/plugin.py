import json
import asyncio
import logging
import glob
import pyee

from sanic import response
from hexi.plugin.InputPlugin import InputPlugin

_logger = logging.getLogger(__name__)

SLEEP_INTERVAL = 1 / 20


class PluginInputFlightAttitude(InputPlugin):

  def __init__(self):
    super().__init__()
    self.configurable = True
    self.connected_clients = set()
    self.current_state = 'initial'
    self.state_running = False
    self.state_progress = 0
    self.states = {}
    self.load_attitudes()
    self.ee = pyee.EventEmitter()
    self.ee.on('state_change', self.on_state_change)

  def activate(self):
    super().activate()
    self.load_attitudes()

  def load_attitudes(self):
    files = glob.glob('./plugins/input_flight_attitude/attitudes/*.json')
    for file_path in files:
      try:
        with open(file_path, 'r') as fd:
          data = json.loads(fd.read())
          self.states[data['id']] = data
      except Exception:
        _logger.error('Cannot load attitude file {0}'.format(file_path))
    _logger.info('Loaded {0} attitudes'.format(len(self.states.keys())))

  def get_states(self):
    data = {
      'current': self.current_state,
      'running': self.state_running,
      'progress': self.state_progress,
      'states': [{
        'id': state['id'],
        'text': state['text'],
        'order': state['order'] if 'order' in state else 0,
        'enabled': (self.current_state in state['fromState']) and not self.state_running,
      } for state_id, state in self.states.items()],
    }
    data['states'].sort(key=lambda state: state['order'])
    return data

  def change_to_state(self, state_id):
    if self.state_running:
      raise Exception('Cannot change state when previous state is running')
    if not (state_id in self.states):
      raise Exception('Invalid state')
    if not (self.current_state in self.states[state_id]['fromState']):
      raise Exception('Cannot change to this state')
    self.state_running = True
    self.current_state = state_id
    self.state_progress = 0
    self.ee.emit('state_change')
    self.send_state_future = asyncio.ensure_future(self.send_signal_async(state_id))
    self.send_state_future.add_done_callback(self.on_send_state_done)

  async def send_signal_async(self, state_id):
    state = self.states[state_id]
    current_step = 0
    all_step = len(state['attitudes'])
    for attitude in state['attitudes']:
      await asyncio.sleep(SLEEP_INTERVAL)
      self.emit_input_signal(attitude[1:])
      # emit step
      current_step = current_step + 1
      if current_step % 20 == 0:
        self.state_progress = current_step / all_step
        self.ee.emit('state_change')

  def on_send_state_done(self, future):
    self.state_running = False
    self.state_progress = 0
    self.ee.emit('state_change')

  def on_state_change(self):
    data_to_send = json.dumps(self.get_states())
    for client in self.connected_clients:
      asyncio.ensure_future(client.send(data_to_send))

  def load(self):
    super().load()

    @self.bp.route('/api/state', methods=['POST'])
    async def set_state(request):
      try:
        if not self.is_activated:
          raise Exception('Please activate this plugin first!')
        state = request.json['state']
        self.change_to_state(state)
        return response.json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Set state failed')
        return response.json({ 'code': 400, 'reason': str(e) })

    @self.bp.websocket('/api/state')
    async def signal_feed(request, ws):
      try:
        self.connected_clients.add(ws)
        await ws.send(json.dumps(self.get_states()))
        while True:
          await ws.recv()
      finally:
        self.connected_clients.remove(ws)
