<div align="center">

<h3 align="center">An AI web agent that applies to jobs for you while you sleep.</h3>
---

## How it works

Give it your resume. It finds the jobs that fit, you pick, and it applies.

| Step | What happens |
|---|---|
| **1. Reads your resume** | Turns it into a search: the titles, the skills and the places that fit you. |
| **2. Searches** | 10 million postings from 24 public sources, rebuilt every day, searched on your computer. |
| **3. Scores** | Reads the best 100 against your resume, then scores the top 25 from 1 to 5, with the gaps and the reasons. |
| **4. You pick** | Select the jobs you want and say yes once. |
| **5. Applies** | A real Firefox opens the company's form, fills every required field, attaches your CV and sends. |
| **6. Keeps the answer** | What each page said, with a screenshot, for every application. |

## Why CareerPilot

- **The company's own form.** No LinkedIn account and no Easy Apply: it applies where the company takes applications.
- **Every posting is tried.** There is no list of sites it refuses, and a site can be taught in one Markdown file: [what has been confirmed](docs/sites.md).
- **A browser built to look like yours.** [invisible-playwright-mcp](https://github.com/feder-cr/invisible_playwright_mcp) is a real Firefox with a person's hands, in a window you can watch.
- **One command.** It installs what it needs, and everything else happens on the screen.

---

## Install

Windows, in PowerShell from the repository folder (runs the local checkout):

```powershell
.\run.ps1
```

Linux:

```bash
curl -LsSf https://raw.githubusercontent.com/feder-cr/Jobs_Applier_AI_Agent/main/run.sh | sh
```

On first run, provide your model API key and resume path. CareerPilot saves them in `~/.careerpilot/.env` and reuses them on later launches. It keeps your extracted CV and search profile in `~/.careerpilot` as well. CareerPilot supports Zro, NVIDIA NIM, OpenRouter, custom OpenAI-compatible endpoints such as OmniRoute, and provider plugins. See [provider setup](docs/providers.md).


---

[Sites](docs/sites.md) · [Configuration](docs/configuration.md) · [Writing a plugin](docs/plugins.md) · [Wiki](https://github.com/feder-cr/Jobs_Applier_AI_Agent/wiki) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=feder-cr/Jobs_Applier_AI_Agent&type=Date&theme=dark">
  <img alt="Star history of CareerPilot" src="https://api.star-history.com/svg?repos=feder-cr/Jobs_Applier_AI_Agent&type=Date" width="100%">
</picture>
