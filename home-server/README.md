# Home server: money stack

Five free, open-source money tools that run on your own computer (later, your home server).
Your bank data never leaves your machine.

| App | What it's for | Address |
|---|---|---|
| [Actual Budget](https://github.com/actualbudget/actual) | Envelope budgeting (YNAB-style): give every dollar a job, track rent, electric, and home-build savings. Start here. | http://localhost:5006 |
| [Firefly III](https://github.com/firefly-iii/firefly-iii) | Full bookkeeping with deep reports and auto-categorizing rules. Takes a weekend to learn. | http://localhost:8080 |
| [Ghostfolio](https://github.com/ghostfolio/ghostfolio) | Investment portfolio tracker (Schwab, Robinhood holdings), entered by hand or CSV. | http://localhost:3333 |
| [Beancount](https://github.com/beancount/beancount) + [Fava](https://github.com/beancount/fava) | Plain-text books in `beancount/main.beancount`; Fava shows the reports. | http://localhost:5000 |
| [OpenBB](https://github.com/OpenBB-finance/OpenBB) | Stock and market research from many data sources, in Python. Pairs with volatile-finder. | (Python, see below) |

You don't need all of them. Most people pick **one** budgeting app (Actual *or* Firefly III *or*
Beancount) plus Ghostfolio for investments. Comment out the ones you don't use in docker-compose.yml.

## Start it (one time, about 20 minutes)
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux).
2. In this folder: `cp .env.example .env`, then fill in every value in `.env`:
   - passwords and secrets: `openssl rand -hex 24` (a different one each line)
   - `FIREFLY_APP_KEY`: exactly 32 characters, `openssl rand -hex 16`
3. `docker compose up -d`, wait a minute, then open the addresses above.
4. Create your account in each app and set a strong password.

## OpenBB (Python, not Docker)
```bash
python3 -m venv ~/openbb-env && source ~/openbb-env/bin/activate
pip install openbb
python -c "from openbb import obb; print(obb.equity.price.historical('AAPL').to_df().tail())"
```
Research only: it shows data, it doesn't tell you what to buy.

## Bank data, safely
- Free path: download CSV statements from your bank and import them (Actual, Firefly III, and
  Ghostfolio all import CSV). About 5 minutes a week.
- Automatic bank sync costs money (Actual's SimpleFIN connection is about $15/year). Optional.
- Never put bank logins or card numbers in any file in this repo. `.env` stays on your machine
  (it's in .gitignore) and Gitleaks blocks secrets from being committed.

## Use it from your phone
The apps only listen on this computer (127.0.0.1) on purpose. To reach them from your phone,
use [Tailscale](https://tailscale.com) (free for personal use) on the computer and the phone, and
change `127.0.0.1:` to your computer's Tailscale address in docker-compose.yml.
Do not forward these ports on your router: that would put your finances on the open internet.

## Backups
`docker compose down`, then copy the Docker volumes (or use each app's export) to a USB drive or
cloud folder once a week. Beancount is just the text file in `beancount/`.

## Updating
`docker compose pull && docker compose up -d`
