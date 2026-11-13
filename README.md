# Playground

Experiments built with Claude, with no plan and no rules. Each folder is one experiment, and every change is checked automatically before it lands.

| Experiment | What it is |
|---|---|
| [night-patrol](night-patrol/) | Flashlight game: find intruders in a dark warehouse at 3 AM. Watch out for the cat. |
| [shorts-studio](shorts-studio/) | Claude Code setup that runs YouTube Shorts in five video types (fragrance, gaming, faceless "what if" simulations, brainrot character stories, anime horror stories): subagents for ideas, scripts, animation, editing, policy checks, and cross-posting, a review memory of every past note, and a debug loop that checks each render frame by frame before it reaches Chris. |
| [home-server](home-server/) | Self-hosted money stack: Actual Budget, Firefly III, Ghostfolio, Beancount + Fava (Docker), plus OpenBB for market research. |
| [volatile-finder](volatile-finder/) | Python CLI that ranks the most volatile liquid stocks right now and backtests putting $1 a day into them. |

Every pull request is checked by CodeQL, Semgrep, Gitleaks, Dependabot, and PR-Agent. See [SECURITY-SETUP.md](SECURITY-SETUP.md).
