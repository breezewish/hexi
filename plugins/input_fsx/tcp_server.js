var net = require('net');

console.log('server created at :4905')

net.createServer(sock => {

  console.log('connected');
  sock.on('data', data => console.log(data.toString()));
  sock.on('close', () => console.log('closed'));

}).listen(4905);
