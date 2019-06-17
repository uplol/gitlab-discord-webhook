# Gitlab Discord Webhooks

I was unsatisifed with the default Discord integration packaged with GitLab, so I decided to make my own handler that forwards events to a Discord webhook.

The goal was to make the webhook match the look-and-feel of the GitHub embed (that Discord provides by appending `/github` to the webhook URL).

## Events
Not all webhook events sent by Gitlab are supported yet. Here's the list of ones available now:
- Push Events
- Pipeline Events

## Setup
You need to set some environemnt variables before running the app.

`DISCORD_WEBHOOK_URL` - The Webhook URL provided by the Discord client
`WEBHOOK_SECRET` - A predefined secret to append to your GitLab webhook URLs

Once set, you can run the `app.py` in the main directory, or run it with the `flask run` utility.