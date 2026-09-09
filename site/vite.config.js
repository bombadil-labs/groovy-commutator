import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { researchWatch } from './scripts/research.mjs';
import { buildResearchProgram } from './scripts/research-program.mjs';
import { readKnowledge, buildKnowledge, knowledgeAsset } from './scripts/knowledge.mjs';

const graph = readKnowledge();
const knowledge = buildKnowledge({ graph });
const research = buildResearchProgram({ knowledge: graph.nodes });

// Curated React pages plus static Research pages generated from Markdown.
// Output goes to ../public (repo root) --
// that directory is gitignored and rebuilt by CI (see
// .github/workflows/pages.yml) rather than committed.
export default defineConfig({
  // Deployed as a GitHub Pages PROJECT site (mbilokonsky.github.io/groovy-commutator/),
  // not a user/root site -- every asset URL Vite emits needs this prefix or
  // it resolves against the domain root instead and 404s (blank page, since
  // the JS bundle never loads). Internal nav links/image src in the
  // components are deliberately relative instead, so they're unaffected by
  // this and would work under any base path.
  base: '/groovy-commutator/',
  plugins: [react(), researchWatch([...research.dependencies, ...knowledge.dependencies]), knowledgeAsset(knowledge.asset)],
  build: {
    outDir: resolve(__dirname, '../public'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        home: resolve(__dirname, 'index.html'),
        concepts: resolve(__dirname, 'concepts.html'),
        questions: resolve(__dirname, 'questions.html'),
        remainder: resolve(__dirname, 'remainder.html'),
        explorer: resolve(__dirname, 'explorer.html'),
        ...research.inputs,
        ...knowledge.inputs,
      },
    },
  },
});
