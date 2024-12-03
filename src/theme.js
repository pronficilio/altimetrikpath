import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2', // Azul
    },
    secondary: {
      main: '#43A047', // Verde
    },
    background: {
      default: '#F5F5F5', // Gris Claro
    },
    text: {
      primary: '#424242', // Gris Oscuro
    },
  },
});

export default theme;
