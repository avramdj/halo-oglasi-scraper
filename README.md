# halo-oglasi-scraper

lil scraper that talks to [discord hooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

make a `config.json` in proj root that looks something like:

```json
{
    "link to halo oglasi URL with filters and stuff": "link to discord hook",
    "link to another URL": "(potentially different) discord hook"
}
```

u can also make an `.env` with SLEEP_TIME and CFG_FILE (points to `/app/config.json` by defaulrt)

then run the compose
