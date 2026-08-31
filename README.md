# NFL Aurora

Small toolchain to pull live NFL scores from ESPN and store them in MySQL.

## What it does

1. `nfl_parser.py pull-games` fetches ESPN scoreboard JSON.
2. It extracts `week`, `status`, home/away team abbreviations, and current scores.
3. It sends each game to the local API (`POST /score`), which upserts into MySQL.
4. `nfl_parser.py clean-games` calls `DELETE /score` on the local API.

## Prerequisites

- Python 3
- Node.js + npm
- MySQL running locally (or Docker)

## Install

### 1. API service (Node + Sequelize)

```bash
cd nflAuroraSequelize
npm install
```

Create database/user matching `nflAuroraSequelize/config/config.json`:

- database: `nflAurora`
- username: `nflAdmin`
- password: `mysql`
- host: `localhost`

You can start MySQL with Docker Compose from the repository root:

```bash
docker compose up -d
```

This starts:
- `mysql` (MySQL database)
- `nfl-api` (Node/Express service on `localhost:3000`)

### 2. Python parser dependencies

From repository root:

```bash
pip3 install requests click python-dateutil pytz
```

## Start the service

In one terminal:

```bash
cd nflAuroraSequelize
npm start
```

The API starts on `http://localhost:3000`.

## Use the tool

From repository root, in another terminal:

```bash
python3 nfl_parser.py pull-games
```

This fetches ESPN data and updates/inserts game rows in the DB via the API.

To run the cleanup call:

```bash
python3 nfl_parser.py clean-games
```
