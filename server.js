const express = require("express");
const PORT = 3001;
const app = express();
const bodyParser = require('body-parser')


// create application/json parser
const jsonParser = bodyParser.json()

//Заголовки для CORS
app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Credentials", true);
  next();
});



app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

let sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('sv.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the database.');
});


function processData(res, sql) {
  db.serialize(function () {
      db.all(sql,
          function (err, rows) {
              if (err) {
                  console.error(err);
                  res.status(500).send(err);
              }
              else
                  sendData(res, rows, err);
          });
  });
}

function sendData(res, data, err) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.send(data);
}


app.get('/parts', function (req, res) {
  processData(res, "SELECT * FROM Parts");
})

app.get('/classes', function (req, res) {
  processData(res, "SELECT * FROM Classes");
})

app.get('/images', function (req, res) {
  processData(res, "SELECT * FROM Images");
})

app.get('/images_categories', function (req, res) {
  processData(res, "SELECT * FROM Images_categories");
})

app.get('/standarts', function (req, res) {
  processData(res, "SELECT * FROM Standarts");
})