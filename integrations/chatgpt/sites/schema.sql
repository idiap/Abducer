-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
-- SPDX-License-Identifier: MIT
CREATE TABLE projects (
  id TEXT PRIMARY KEY,
  owner_id TEXT NOT NULL,
  title TEXT NOT NULL,
  question TEXT NOT NULL,
  revision INTEGER NOT NULL DEFAULT 1,
  notes TEXT NOT NULL DEFAULT '[]',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX projects_owner ON projects (owner_id, updated_at);
