## Dependabot Scorecards

Want a quick view of your dependabot data to prioritize bad repos?

Create a `repos.txt` with GitHub repos in the following format:

```
django/django
facebook/react
```

Then run the following commands:

```bash
script/download
script/server
```

## Requirements
Flask and a configured `gh cli` client
