# VACOP Frontend

This directory contains the frontend application for the VACOP project, built with React, TypeScript, and Vite.

## Project Structure

- `VACOP-app/`: The main application source code.

## Development Setup

### Run with Docker (recommended)

The frontend is meant to be started together with the backend using Docker Compose from the project root (`VACOP_Dashboard/`).

From `VACOP_Dashboard/`:

```bash
docker compose up --build
```

Then open: http://localhost/

To stop:

```bash
docker compose down
```

See the full run guide: `../DOCS_RUN.md`.

### Run locally (without Docker)

Prerequisites:

- Node.js (LTS recommended)
- npm (comes with Node.js)

From this folder:

```bash
cd VACOP-app
npm install
npm run dev
```

Then open the Vite dev server URL (usually http://localhost:5173/).

Notes:

- Some pages call the backend at `http://localhost:5000`.
	- Option A: start the full stack with Docker (recommended): see `../DOCS_RUN.md`.
	- Option B: start the backend separately (Python/Docker) so `http://localhost:5000` is reachable.