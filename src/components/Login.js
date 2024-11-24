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
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
    },
    validationSchema: Yup.object({
      email: Yup.string()
        .email('Email inválido')
        .required('Campo requerido'),
      password: Yup.string()
        .min(6, 'Mínimo 6 caracteres')
        .required('Campo requerido'),
    }),
    onSubmit: (values) => {
      console.log("Iniciando sesión con:", values);
      // Lógica para manejar el inicio de sesión
      axios
        .post('http://localhost:5000/api/auth/login', values)
        .then((response) => {
          const token = response.data.token; // Obtener el token
          localStorage.setItem('token', token); // Guardar el token
          navigate('/profile'); // Redirigir al perfil
        })
        .catch((error) => {
          console.error(
            'Error al iniciar sesión:',
            error.response?.data || error.message
          );
          alert(error.response?.data?.msg || 'Error al iniciar sesión');
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
          Iniciar Sesión
        </Typography>
        <form onSubmit={formik.handleSubmit} noValidate>
          <TextField
            margin="normal"
            fullWidth
            id="email"
            name="email"
            label="Correo Electrónico"
            value={formik.values.email}
            onChange={formik.handleChange}
            error={formik.touched.email && Boolean(formik.errors.email)}
            helperText={formik.touched.email && formik.errors.email}
          />
          <TextField
            margin="normal"
            fullWidth
            name="password"
            label="Contraseña"
            type="password"
            id="password"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.touched.password && Boolean(formik.errors.password)}
            helperText={formik.touched.password && formik.errors.password}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >
            Iniciar Sesión
          </Button>
          <Box sx={{ mt: 2 }} />
          <Typography variant="body2" align="center">
            ¿No tienes una cuenta? <Link to="/">Regístrate</Link>
          </Typography>
        </form>
      </Box>
    </Container>
  );
}

export default Login;
