import { dirname } from REMOVED_SECRETpathREMOVED_SECRET;
import { fileURLToPath } from REMOVED_SECRETurlREMOVED_SECRET;
import { FlatCompat } from REMOVED_SECRET@eslint/eslintrcREMOVED_SECRET;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [...compat.extends(REMOVED_SECRETnext/core-web-vitalsREMOVED_SECRET)];

export default eslintConfig;
