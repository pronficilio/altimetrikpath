import React from 'react';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Register() {
  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      password: '',
    },
    validationSchema: Yup.object({
      name: Yup.string().required('Campo requerido'),
      email: Yup.string()
        .email('Email inválido')
        .required('Campo requerido'),
      password: Yup.string()
        .min(6, 'Mínimo 6 caracteres')
        .required('Campo requerido'),
    }),
    onSubmit: (values) => {
      axios
        .post('http://localhost:5000/api/users', values)
        .then((response) => {
          console.log('Usuario registrado:', response.data);
        })
        .catch((error) => {
          console.error('Error al registrar el usuario:', error);
        }); 
    },
  });

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          padding: 4,
          backgroundColor: 'white',
          borderRadius: 2,
          boxShadow: 3,
        }}
      >
        <Typography component="h1" variant="h5" align="center" gutterBottom>
          Registro
        </Typography>
        <form onSubmit={formik.handleSubmit} noValidate>
          <TextField
            margin="normal"
            required
            fullWidth
            id="name"
            label="Nombre"
            name="name"
            value={formik.values.name}
            onChange={formik.handleChange}
            error={formik.touched.name && Boolean(formik.errors.name)}
            helperText={formik.touched.name && formik.errors.name}
            autoComplete="name"
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Correo Electrónico"
            name="email"
            value={formik.values.email}
            onChange={formik.handleChange}
            error={formik.touched.email && Boolean(formik.errors.email)}
            helperText={formik.touched.email && formik.errors.email}
            autoComplete="email"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.touched.password && Boolean(formik.errors.password)}
            helperText={formik.touched.password && formik.errors.password}
            label="Contraseña"
            type="password"
            id="password"
            autoComplete="new-password"
          />
          <Box sx={{ mt: 2 }} />
          <Typography variant="body2" color="textSecondary" align="center">
            Al registrarte, aceptas nuestras Condiciones de uso y Política de
            privacidad.
          </Typography>
          <Box sx={{ mt: 2 }} />
          <Typography variant="body2" color="textSecondary" align="center">
            ¿Ya tienes una cuenta? <Link to="/login">Inicia sesión</Link>
          </Typography>
          <Box sx={{ mt: 2 }} />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >
            Registrarse
          </Button>
        </form>
      </Box>
    </Container>
  );
}

export default Register;
