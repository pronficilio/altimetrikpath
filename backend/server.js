const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('146.190.175.146-key.pem'),
  cert: fs.readFileSync('146.190.175.146.pem'),
};

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;
const HTTPS_PORT = process.env.HTTPS_PORT || 5444;

// Middlewares
app.use(cors());
app.use(express.json());

// Conexión a la Base de Datos
mongoose
  .connect(process.env.MONGO_URI, {
    dbName: 'altimetrik'
  })
  .then(() => console.log('Conectado a MongoDB'))
  .catch((err) => console.error('Error al conectar a MongoDB:', err));

// Rutas
app.use('/api/users', require('./routes/users'));
app.use('/api/auth', require('./routes/auth'));

// Iniciar el servidor HTTP
app.listen(PORT, () => {
  console.log(`Servidor HTTP corriendo en el puerto ${PORT}`);
});

// Iniciar el servidor HTTPS
https.createServer(options, app).listen(HTTPS_PORT, () => {
  console.log(`Servidor HTTPS corriendo en el puerto ${HTTPS_PORT}`);
});