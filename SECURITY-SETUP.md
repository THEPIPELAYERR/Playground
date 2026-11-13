# Security setup for this repo

These run automatically on every pull request and push (files in .github/):

| Tool | What it catches | Cost |
|---|---|---|
| CodeQL (`codeql.yml`) | Security bugs in Python, JavaScript, and the workflows themselves. Results: Security tab → Code scanning. | Free (public repo) |
| Semgrep (`semgrep.yml`) | Rule-based security and bug patterns. Fails the check if it finds something. | Free |
| Gitleaks (`gitleaks.yml`) | API keys, passwords, and tokens in commits. Also runs daily. | Free (personal account) |
| Dependabot (`dependabot.yml`) | Outdated or vulnerable packages and actions; opens update PRs weekly. | Free |
| PR-Agent (`pr-agent.yml`) | AI review, summary, and suggestions on every PR, using Claude. | A few cents of API use per PR |

## Two minutes of clicks Chris has to do (GitHub doesn't let Claude change repo settings)
1. **Settings → Advanced Security** (or "Code security"): turn on **Dependabot alerts**,
   **Dependabot security updates**, **Secret scanning**, and **Push protection**.
2. **PR-Agent key:** create an API key at console.anthropic.com, then
   **Settings → Secrets and variables → Actions → New repository secret**, name `ANTHROPIC_KEY`.
   Until it's added, PR-Agent skips itself instead of failing.
   To make reviews cheaper, change `config.model` in pr-agent.yml to a smaller Claude model.
