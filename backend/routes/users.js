const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const dotenv = require('dotenv');
const auth = require('../middleware/auth');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');

dotenv.config();

// Registro de Usuario
router.post('/', async (req, res) => {
  const { name, email, password } = req.body;

  try {
    // Verificar si el usuario ya existe
    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ msg: 'El usuario ya existe' });
    }

    user = new User({
      name,
      email,
      password,
    });

    // Encriptar la contraseña
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(password, salt);

    await user.save();

    // Crear y devolver el JWT
    const payload = {
      user: {
        id: user.id,
      },
    };

    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      { expiresIn: 3600 },
      (err, token) => {
        if (err) throw err;
        res.json({ token });
      }
    );
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Error en el servidor');
  }
});

// Actualizar Usuario
router.put('/', auth, async (req, res) => {
  const { name, email } = req.body;
  try {
    console.log(req.user.id);
    const user = await User.findByIdAndUpdate(
      req.user.id,
      { name, email },
      { new: true }
    ).select('-password');
    res.json(user);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Error en el servidor');
  }
});

// Cambiar Contraseña
router.put('/change-password', auth, async (req, res) => {
  const { currentPassword, newPassword } = req.body;
  try {
    const user = await User.findById(req.user.id);
    if (!user) {
      return res.status(404).json({ msg: 'Usuario no encontrado' });
    }
    const isMatch = await bcrypt.compare(currentPassword, user.password);
    if (!isMatch) {
      return res.status(400).json({ msg: 'Contraseña actual incorrecta' });
    }
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(newPassword, salt);
    await user.save();
    res.json({ msg: 'Contraseña actualizada correctamente' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Error en el servidor');
  }
});

// Configuración de almacenamiento y restricciones con multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${req.user.id}-${Date.now()}-${file.originalname}`);
  },
});

const fileFilter = (req, file, cb) => {
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Tipo de archivo no permitido'), false);
  }
};

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter,
});

// Ruta para subir el CV
router.post('/upload-cv', auth, upload.single('cv'), async (req, res) => {
  try {
    // Guardar la ruta del archivo en el perfil del usuario
    let user = await User.findById(req.user.id);
    const filePath = req.file.path;
    user.cv = filePath;
    user.original_cv = req.file.originalname;
    await user.save();

    // Invocar el script de análisis de CV
    try {
      const stdout = execFileSync('/root/miniconda3/envs/altimetrikenv/bin/python', ['parse_cv.py', filePath]);
      
      console.log(stdout);
      const extractedData = JSON.parse(stdout);

      console.log("ojo aqui: ", extractedData);
      // Actualizar el perfil del usuario
      user.experience = extractedData.total_experience;
      user.skills = extractedData.skills;
      user.education = extractedData.education;
      user.certifications = extractedData.career_path;
      user.projects = extractedData.projects;
      user.languages = extractedData.languages;
      await user.save();

      res.json({
        msg: 'CV procesado correctamente',
        data: extractedData,
      });
    } catch (error) {
      console.error('Error al ejecutar el script de Python:', error);
      return res.status(500).send('Error al procesar el CV');
    }

    res.json({ msg: 'CV subido correctamente', path: req.file.path });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Error en el servidor');
  }
});

module.exports = router;
