import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Modal,
  TextField,
  LinearProgress,
  Snackbar,
  Alert
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';

function Profile() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [editOpen, setEditOpen] = useState(false);
  const [passwordOpen, setPasswordOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleEditOpen = () => setEditOpen(true);
  const handleEditClose = () => setEditOpen(false);
  const handlePasswordOpen = () => setPasswordOpen(true);
  const handlePasswordClose = () => setPasswordOpen(false);

  const formik = useFormik({
    initialValues: {
      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',
    },
    validationSchema: Yup.object({
      currentPassword: Yup.string().required('Campo requerido'),
      newPassword: Yup.string()
        .min(6, 'Mínimo 6 caracteres')
        .required('Campo requerido'),
      confirmNewPassword: Yup.string()
        .oneOf([Yup.ref('newPassword'), null], 'Las contraseñas no coinciden')
        .required('Campo requerido'),
    }),
    onSubmit: (values) => {
      axios
        .put('http://localhost:5000/api/users/change-password', values, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          }
        })
        .then((response) => {
          console.log('Contraseña actualizada:', response.data);
          setSnackbar({
            open: true,
            message: response.data.msg,
            severity: 'success',
          });
          setPasswordOpen(false);
          formik.resetForm();
        })
        .catch((error) => {
          console.error('Error al cambiar la contraseña:', error);
          setSnackbar({
            open: true,
            message: 'Error al cambiar la contraseña',
            severity: 'error',
          });
        });
    },
  });

  const handleUpdate = (event) => {
    event.preventDefault();
    axios
      .put('http://localhost:5000/api/users', user, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
      })
      .then((response) => {
        setUser(response.data);
        handleEditClose();
        setSnackbar({
          open: true,
          message: 'Información actualizada correctamente',
          severity: 'success',
        });
      })
      .catch((error) => {
        console.error('Error al actualizar la información:', error);
        setSnackbar({
          open: true,
          message: 'Error al actualizar la información',
          severity: 'error',
        });
      });
  };

  const uploadCV = (file) => {
    const formData = new FormData();
    formData.append('cv', file);
    axios
      .post('https://localhost:5443/api/users/upload-cv', formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        }
      })
      .then((response) => {
        console.log('CV subido:', response.data);
        setUploadProgress(0);
        setSnackbar({
          open: true,
          message: 'CV subido correctamente',
          severity: 'success',
        });
      })
      .catch((error) => {
        console.error('Error al subir el CV:', error);
        setUploadProgress(0);
        setSnackbar({
          open: true,
          message: 'Error al subir el CV',
          severity: 'error',
        });
      });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      ];
      const maxSize = 5 * 1024 * 1024; // 5MB

      if (!allowedTypes.includes(file.type)) {
        alert('Tipo de archivo no permitido. Solo .pdf, .doc, .docx');
        return;
      }

      if (file.size > maxSize) {
        alert('El archivo supera el tamaño máximo de 5MB.');
        return;
      }

      uploadCV(file);
      e.target.value = '';
    } 
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  useEffect(() => {
    axios
      .get('http://localhost:5000/api/auth', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
      })
      .then((response) => {
        setUser(response.data);
      })
      .catch((error) => {
        console.error('Error al obtener el usuario:', error);
        navigate('/login');
      });
  }, [navigate]);

  if (!user) {
    return <Typography>Cargando...</Typography>;
  }

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
        <Typography variant="h4" gutterBottom>
          Bienvenido, {user.name}
        </Typography>

        <Typography variant="h4" gutterBottom>
          Perfil de Usuario
        </Typography>

        <Button variant="contained" onClick={handleEditOpen}>
          Editar Información
        </Button>
        <Button variant="contained" onClick={handlePasswordOpen} sx={{ mt: 2 }}>
          Cambiar Contraseña
        </Button>
        <Button variant="contained" component="label">
          Subir CV
          <input type="file" hidden accept=".pdf,.docx" onChange={handleFileChange} />
        </Button>
        <Modal open={passwordOpen} onClose={handlePasswordClose}>
          <Box sx={{ ...modalStyles }}>
            <Typography variant="h6">Cambiar Contraseña</Typography>
            <form onSubmit={formik.handleSubmit} noValidate>
              <TextField
                fullWidth
                margin="normal"
                name="currentPassword"
                label="Contraseña Actual"
                type="password"
                value={formik.values.currentPassword}
                onChange={formik.handleChange}
                error={
                  formik.touched.currentPassword &&
                  Boolean(formik.errors.currentPassword)
                }
                helperText={
                  formik.touched.currentPassword && formik.errors.currentPassword
                }
              />
              <TextField
                fullWidth
                margin="normal"
                name="newPassword"
                label="Nueva Contraseña"
                type="password"
                value={formik.values.newPassword}
                onChange={formik.handleChange}
                error={
                  formik.touched.newPassword && Boolean(formik.errors.newPassword)
                }
                helperText={
                  formik.touched.newPassword && formik.errors.newPassword
                }
              />
              <TextField
                fullWidth
                margin="normal"
                name="confirmNewPassword"
                label="Confirmar Nueva Contraseña"
                type="password"
                value={formik.values.confirmNewPassword}
                onChange={formik.handleChange}
                error={
                  formik.touched.confirmNewPassword &&
                  Boolean(formik.errors.confirmNewPassword)
                }
                helperText={
                  formik.touched.confirmNewPassword &&
                  formik.errors.confirmNewPassword
                }
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                sx={{ mt: 3 }}
              >
                Cambiar Contraseña
              </Button>
            </form>
          </Box>
        </Modal>
        <Modal open={editOpen} onClose={handleEditClose}>
          <Box sx={{ ...modalStyles }}>
            <Typography variant="h6">Editar Información</Typography>
            <form onSubmit={handleUpdate}>
              <TextField
                fullWidth
                margin="normal"
                label="Nombre"
                value={user?.name || ''}
                onChange={(e) => setUser({ ...user, name: e.target.value })}
              />
              <TextField
                fullWidth
                margin="normal"
                label="Correo Electrónico"
                value={user?.email || ''}
                onChange={(e) => setUser({ ...user, email: e.target.value })}
              />
              <Button type="submit" variant="contained" color="primary">
                Guardar Cambios
              </Button>
            </form>
          </Box>
        </Modal>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Nombre:</strong> {user.name}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Correo:</strong> {user.email}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="secondary"
              onClick={handleLogout}
              sx={{ mt: 3 }}
            >
              Cerrar Sesión
            </Button>
          </Grid>
        </Grid>
      </Box>
      {uploadProgress > 0 && (
        <Box sx={{ width: '100%', mt: 2 }}>
          <LinearProgress variant="determinate" value={uploadProgress} />
          <Typography variant="body2" color="text.secondary">
            Subiendo: {uploadProgress}%
          </Typography>
        </Box>
      )}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={8000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}
const modalStyles = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};
export default Profile;