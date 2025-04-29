import js from "@eslint/js";
import globals from "globals";
import pluginReact, { rules } from "eslint-plugin-react";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: { js },
    extends: ["js/recommended"],
  },
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: { globals: globals.browser },
  },
  pluginReact.configs.flat.recommended,
  {
    rules: {
      "semi": ["error", "always"],
      "prefer-const": "error",
      "quotes": ["error", "double"]
    },
  },
]);
