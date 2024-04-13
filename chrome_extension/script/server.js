// server.js
const express = require('express');
const WebSocket = require('ws');
const http = require('http');
const bodyParser = require('body-parser'); // Ensure body-parser is installed

const app = express();
app.use(bodyParser.json()); // for parsing application/json

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', ws => {
  console.log('WebSocket connection established');
});

// Endpoint for refreshing the current tab with a new URL
app.post('/refresh-url', (req, res) => {
  const { url } = req.body;
  // Broadcast the URL to all WebSocket clients with type 'url' for refreshing
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ type: 'url', data: url }));
    }
  });
  res.send('URL sent for refresh');
});

// Endpoint for opening a new tab with a URL
app.post('/open-url', (req, res) => {
  const { url } = req.body;
  // Broadcast the URL to all WebSocket clients with type 'new-url' for opening in a new tab
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ type: 'new-url', data: url }));
    }
  });
  res.send('URL sent for opening in new tab');
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});
