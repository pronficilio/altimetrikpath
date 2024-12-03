import React from 'react';
import { Container, Typography, Box } from '@mui/material';

function PrivacyPolicy() {
  return (
    <Container maxWidth="md">
      <Box sx={{ marginTop: 8, padding: 4, backgroundColor: 'white', borderRadius: 2, boxShadow: 3 }}>
        <Typography variant="h4" gutterBottom>
          Políticas de Privacidad
        </Typography>
        <Typography variant="body1" paragraph>
          En nuestra aplicación, valoramos tu privacidad y nos comprometemos a proteger tus datos personales. Esta política de privacidad describe cómo manejamos y protegemos tu información.
        </Typography>
        <Typography variant="h6" gutterBottom>
          Recopilación de Datos
        </Typography>
        <Typography variant="body1" paragraph>
          Recopilamos información personal que nos proporcionas directamente, como tu nombre, correo electrónico y contraseña cuando te registras en nuestra aplicación.
        </Typography>
        <Typography variant="h6" gutterBottom>
          Uso de Datos
        </Typography>
        <Typography variant="body1" paragraph>
          Utilizamos tus datos personales para proporcionarte acceso a nuestra aplicación, mejorar nuestros servicios y comunicarnos contigo.
        </Typography>
        <Typography variant="h6" gutterBottom>
          Protección de Datos
        </Typography>
        <Typography variant="body1" paragraph>
          Implementamos medidas de seguridad para proteger tus datos personales contra el acceso no autorizado, la alteración, divulgación o destrucción.
        </Typography>
        <Typography variant="h6" gutterBottom>
          Contacto
        </Typography>
        <Typography variant="body1" paragraph>
          Si tienes alguna pregunta sobre nuestras políticas de privacidad, por favor contáctanos a través de nuestro correo electrónico de soporte.
        </Typography>
      </Box>
    </Container>
  );
}

export default PrivacyPolicy;