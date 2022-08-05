const express = require("express");
const PORT = 3001;
const app = express();
const bodyParser = require('body-parser')
const csv = require('csv-parser')
const fs = require('fs')


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

const parts = [];
// fs.createReadStream('Data.csv')
//   .pipe(csv({ separator: ';' }))
//   .on('data', (data) => parts.push(data))
//   .on('end', () => {
//     console.log("parts ok")
//   });
fs.createReadStream('Parts.csv')
  .pipe(csv({ separator: ';' }))
  .on('data', (data) => parts.push(data))
  .on('end', () => {
    console.log("parts ok")
  });
const standarts = [];
fs.createReadStream('Standarts.csv')
  .pipe(csv({ separator: ';' }))
  .on('data', (data) => standarts.push(data))
  .on('end', () => {
    console.log("standarts ok")
  });
const classes = [];
fs.createReadStream('Classes.csv')
  .pipe(csv({ separator: ';' }))
  .on('data', (data) => classes.push(data))
  .on('end', () => {
    console.log("classes ok")
  });
const im_categories = [];
fs.createReadStream('Images_categories.csv')
  .pipe(csv({ separator: ';' }))
  .on('data', (data) => im_categories.push(data))
  .on('end', () => {
    console.log("categories ok")
  });
// const images = [];
// fs.createReadStream('Images.csv')
//   .pipe(csv({ separator: ';' }))
//   .on('data', (data) => images.push(data))
//   .on('end', () => {
//     console.log("images ok")
//   });

function getClass(class_id) {
  return classes.map(sas=>{
    if(sas.id==class_id) return sas.name
  }).filter(anyValue => typeof anyValue !== 'undefined')[0]
}

function getStandart(standart_id) {
  return standarts.map(sas=>{
    if(sas.id==standart_id) return sas.name
  }).filter(anyValue => typeof anyValue !== 'undefined')[0]
}

function getImages(part_id) {
  cat_id=parts.map(sas=>{
    if(sas.id==part_id) 
      return sas.image_category
  }).filter(anyValue => typeof anyValue !== 'undefined')[0]

  cat_name=im_categories.map(sas=>{
    if(sas.id==cat_id) 
      return sas.folder
  }).filter(anyValue => typeof anyValue !== 'undefined')[0]
  // return images.map(sas=>{
  //   if(sas.category_id==cat_id) return cat_name+'/'+sas.image_name
  // }).filter(anyValue => typeof anyValue !== 'undefined')
  data=fs.readdirSync(cat_name+'/');
  return  data.map(sas=>{
    return cat_name+'/'+sas
  })
}


app.get('/parts', function (req, res) {
  data1=[]
  for(let i=0; i<parts.length; i++){
    data1.push({id: parts[i].id, class: getClass(parts[i].class_id), standart: getStandart(parts[i].standart_id), size: parts[i].size, images: getImages(parts[i].id)})
  }
  sendData(res, data1);
})

app.use('/images', express.static('Images'));