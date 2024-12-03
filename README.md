"""
# AltiMetrikPath

AltiMetrikPath es una aplicación web diseñada para ayudar a los empleados a generar planes de carrera personalizados basados en su perfil individual. A través del análisis del CV del usuario y mediante el uso de inteligencia artificial, la aplicación proporciona recomendaciones para establecer un plan de nivelación y crecimiento profesional.

Montado en: http://146.190.175.146:3000/

## Características

- **Registro e Inicio de Sesión**: Los usuarios pueden crear una cuenta y acceder de forma segura a sus perfiles.
- **Perfil de Usuario**: Visualización y edición de información personal, incluyendo la carga de CV.
- **Carga y Análisis de CV**: Los usuarios pueden subir su CV en formato PDF o DOCX. El sistema extrae información relevante utilizando `ResumeParser` y modelos de IA.
- **Generación de Plan de Carrera**: Basado en los datos extraídos del CV y con la ayuda de ChatGPT, la aplicación sugiere rutas de carrera y niveles adecuados para el usuario.
- **Seguridad**: Autenticación segura utilizando JWT, encriptación de contraseñas y manejo seguro de datos sensibles.

## Tecnologías Utilizadas

- **Frontend**:
  - React.js con Material-UI para la interfaz de usuario.
  - Formik y Yup para la gestión y validación de formularios.
  - Axios para las solicitudes HTTP.
- **Backend**:
  - Node.js y Express para el servidor.
  - MongoDB y Mongoose para la base de datos.
  - Bcrypt.js para encriptación de contraseñas.
  - Jsonwebtoken para autenticación JWT.
  - Multer para manejo de cargas de archivos.
  - Python y PyResparser para la extracción de datos del CV.
  - OpenAI API para interacción con ChatGPT.

## Script principal

La función en backend/parse_cv.py analiza los elementos de position en tres categorías: tools, programmingLanguages y skillsResponsibilities. Para cada categoría, realiza las siguientes acciones:

- Incrementa `total_items` si el elemento no es opcional.
- Compara cada elemento con las coincidencias en los diccionarios correspondientes (`tools_matches`, `languages_matches`, `skills_matches`).
    - Si hay una coincidencia explícita, suma 1 al `total_score`.
    - Si hay una coincidencia implícita, suma 0.8 al `total_score`.
    - Si hay una coincidencia probable, suma 0.5 al `total_score`.
    - Si no hay coincidencia, agrega el elemento a `missing_tools`, `missing_languages` o `missing_skills` según corresponda.

En resumen, la función calcula una puntuación total que representa el grado de coincidencia entre las habilidades del candidato y los requisitos del puesto, almacenando también las habilidades faltantes.

## Instalación y Ejecución

# Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/altimetrikpath.git
```

# Entrar al directorio del frontend
```bash
cd altimetrikpath
```

# Instalar dependencias del frontend
```bash
npm install
```

# Iniciar el servidor de desarrollo del frontend
```bash
npm start
```

# En otra terminal, entrar al directorio del backend
```bash
cd backend
```

# Instalar dependencias del backend
```bash
npm install
```

# Configurar variables de entorno en backend/.env
# MONGO_URI, JWT_SECRET, OPENAI_API_KEY

# Instalar dependencias de Python para el análisis del CV
```bash
pip install pyresparser spacy
python -m spacy download en_core_web_sm
```

# Iniciar el servidor del backend
```bash
node server.js
```

## Uso

1. **Registro**: Crear una cuenta proporcionando nombre, correo electrónico y contraseña.
2. **Inicio de Sesión**: Acceder con las credenciales registradas.
3. **Perfil**: Completar o actualizar información personal.
4. **Carga de CV**: Subir el CV en formato PDF o DOCX.
5. **Análisis de CV**: El sistema procesará el CV y extraerá información relevante.
6. **Generación de Plan de Carrera**: Basado en el análisis, el sistema sugerirá un plan de carrera y nivelación.

## Estructura del Proyecto

- **/frontend**: Código fuente del frontend en React.
- **/backend**: Código fuente del backend en Node.js y Express.
- **/backend/parse_cv.py**: Script en Python para analizar el CV.

## Contribución

Las contribuciones son bienvenidas. Por favor, crea una rama nueva para tus cambios y envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.