const express = require('express');
const app = express();
const port = 5000;
const path = require('path');

// const cors = require('cors');

// app.use(cors({
//   'origin': 'http://localhost:5000/api/recipes'
// }));

app.use('/static', express.static(path.join(__dirname + '/js')));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, '/index.html'));
});

app.listen(port, () => {
  console.log(`CORS Enabled listening on port ${port}`);
});
