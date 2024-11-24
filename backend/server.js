const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middlewares
app.use(cors());
app.use(express.json());

// Conexión a la Base de Datos
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    dbName: 'altimetrik'
  })
  .then(() => console.log('Conectado a MongoDB'))
  .catch((err) => console.error('Error al conectar a MongoDB:', err));

// Rutas
app.use('/api/users', require('./routes/users'));
app.use('/api/auth', require('./routes/auth'));

app.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});