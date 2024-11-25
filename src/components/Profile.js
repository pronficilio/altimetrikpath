import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Modal,
  TextField,
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Profile() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [editOpen, setEditOpen] = useState(false);
  const [passwordOpen, setPasswordOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const handleEditOpen = () => setEditOpen(true);
  const handleEditClose = () => setEditOpen(false);
  const handlePasswordOpen = () => setPasswordOpen(true);
  const handlePasswordClose = () => setPasswordOpen(false);

  const handlePasswordChange = (event) => {
    event.preventDefault();
    axios
      .put(
        'http://localhost:5000/api/auth/password',
        { currentPassword, newPassword },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          }
        }
      )
      .then((response) => {
        alert(response.data.msg);
        setPasswordOpen(false);
      })
      .catch((error) => console.error(error));
  };

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
      })
      .catch((error) => console.error(error));
  };

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file && (file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      console.log('Archivo válido', file);
    } else {
      alert('Sube un archivo PDF o DOCX.');
    }
  }

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

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

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
            <form onSubmit={handlePasswordChange}>
              <TextField
                fullWidth
                margin="normal"
                label="Contraseña Actual"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
              <TextField
                fullWidth
                margin="normal"
                label="Nueva Contraseña"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <TextField
                fullWidth
                margin="normal"
                label="Confirmar Nueva Contraseña"
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
              />
              <Button type="submit" variant="contained" color="primary">
                Guardar Cambios
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