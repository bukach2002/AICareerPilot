# Configuration

Press `e` in CareerPilot to change these on the screen. CareerPilot reads `careerpilot.yaml` in its folder, `~/.careerpilot` by default. A missing file, or a missing key, takes the default below. Restart `careerpilot` after you edit the file.

Loading a resume rewrites this file, and the rewrite drops the comments you put in it, so keep your notes elsewhere.

CareerPilot uses OpenAI-compatible model APIs. On first use, the selected provider's API key and source resume path are saved in `~/.careerpilot/.env` and reused on later launches. The extracted CV and search profile are kept in `~/.careerpilot` too. A provider's key environment variable and `CAREERPILOT_RESUME_PATH` override the saved values. See [Providers](providers.md) for supported providers and extensions.

| Key | Default | What it does |
|---|---|---|
| `provider` | `zro` | OpenAI-compatible provider ID: `zro`, `nvidia`, `openrouter`, `custom`, or an installed provider plugin. |
| `api_base_url` | provider default | Optional API base URL override. Set it for `custom` providers such as a local OmniRoute server. |
| `name` | empty | Your name for this search, shown at the top of the list. |
| `goals` | empty | What you are looking for, in your own words. The decision model and the judge read it. |
| `database` | `https://github.com/feder-cr/Jobs_Applier_AI_Agent/releases/download/jobs-latest/manifest.json` | Where the job database is: the URL of its `manifest.json`, or the path of a local one. The files it names sit beside it, unless its `base_url` says otherwise. |
| `max_age_days` | `60` | Postings posted more than this many days ago are left out. A posting with no date is kept. |
| `model` | `deepseek-v4.1-flash` | Fills the application forms. |
| `quick_model` | `deepseek-v4.1-flash` | Writes the search plan from your CV, and the other short calls of a search. |
| `judge_model` | `deepseek-v4.1-flash` | Writes the score and the report of each shortlisted posting. |
| `decision_model` | `deepseek-v4.1-flash` | Answers the six questions that shortlist the postings. |
| `filters.include` | empty | Title words to search for. With no `plan`, each word is one title. CareerPilot asks for a resume until there is a CV and at least one of these. |
| `filters.exclude` | empty | Whole words: a posting whose title has one of them is left out. |
| `filters.locations` | empty | Places a posting's location must name, as whole words. |
| `filters.countries` | empty | Countries. A posting in one of them passes. With `locations`, a posting that names one of those places passes only if its country is empty or one of these. |
| `filters.cities` | empty | Cities. A posting whose location names one ranks higher; others are not left out. |
| `filters.plan` | empty | The title plan, with `nodes` and `arcs`. Each node has an `id`, a `weight` and `forms`, the wordings with their weights; a node of weight 0 only conditions the arcs. Each arc has `when` or `unless` (a node or a phrase in the title) and `then`, a list of `target` and `multiplier`; the target `*` is the whole title. Empty: the plan is `filters.include`. |
