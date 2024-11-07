import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";
import pluginPrettier from "eslint-plugin-prettier";
import configPrettier from "eslint-config-prettier";

/** @type {import('eslint').Linter.Config[]} */
export default [
  { files: ["**/*.{js,mjs,cjs,jsx}"] },
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  pluginReact.configs.flat.recommended,
  pluginPrettier, // Activa el plugin de Prettier
  configPrettier, // Desactiva las reglas de ESLint que interfieren con Prettier
  {
    rules: {
      "prettier/prettier": "error" // Asegura que los errores de formato sean reportados
    }
  }
];
