
import express from 'express';
import bodyParser from 'body-parser';
import dotenv from 'dotenv';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';
dotenv.config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));

app.post('/api/v1/auth/login', (req, res) => {
  const { email } = req.body;
  if (!email) return res.status(400).json({ error: 'email required' });
  return res.json({ token: 'stub-jwt-token', user: { id: uuidv4(), email } });
});

app.post('/api/v1/companies', (req, res) => {
  const body = req.body;
  const id = uuidv4();
  return res.status(201).json({ id, ...body });
});

import multer from 'multer';
const upload = multer({ dest: '/tmp/uploads' });
app.post('/api/v1/uploads', upload.array('files'), (req, res) => {
  return res.json({ status: 'received', files: (req.files || []).length });
});

const port = process.env.PORT || 4000;
app.listen(port, () => console.log(`Backend running on port ${port}`));
