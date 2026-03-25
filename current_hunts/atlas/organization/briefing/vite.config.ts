import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

function walkDir(dir: string, depth = 0): any[] {
  if (depth > 5) return [];
  const skip = new Set(['node_modules', '.git', '__pycache__', '.DS_Store', '.mockups', '.claude']);
  try {
    return fs.readdirSync(dir)
      .filter(name => !skip.has(name) && !name.startsWith('.'))
      .sort((a, b) => {
        const aDir = fs.statSync(path.join(dir, a)).isDirectory();
        const bDir = fs.statSync(path.join(dir, b)).isDirectory();
        if (aDir !== bDir) return aDir ? -1 : 1;
        return a.localeCompare(b);
      })
      .map(name => {
        const full = path.join(dir, name);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
          return { name, type: 'dir', children: walkDir(full, depth + 1) };
        }
        return { name, type: 'file' };
      });
  } catch { return []; }
}

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'tree-api',
      configureServer(server) {
        const scienceDir = path.resolve(__dirname, '../../..');

        server.middlewares.use('/api/tree', (_req, res) => {
          const tree = walkDir(scienceDir);
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ root: 'science', children: tree }));
        });

        server.middlewares.use('/api/file', (req, res) => {
          const filePath = decodeURIComponent(req.url?.replace(/^\//, '') || '');
          const full = path.resolve(scienceDir, filePath);
          if (!full.startsWith(scienceDir)) {
            res.statusCode = 403;
            res.end('Forbidden');
            return;
          }
          if (!fs.existsSync(full)) {
            res.statusCode = 404;
            res.end('Not found');
            return;
          }
          const ext = path.extname(full).toLowerCase();
          const mimeTypes: Record<string, string> = {
            '.html': 'text/html',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.json': 'application/json',
            '.md': 'text/plain; charset=utf-8',
            '.py': 'text/plain; charset=utf-8',
          };
          res.setHeader('Content-Type', mimeTypes[ext] || 'application/octet-stream');
          res.end(fs.readFileSync(full));
        });
      },
    },
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
