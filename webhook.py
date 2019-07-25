from datetime import datetime, timedelta

from disco.types.message import MessageEmbed
from disco.types.webhook import Webhook

COLOR_BLUE = 4359924
COLOR_RED = 16711680
COLOR_GREEN = 58631
COLOR_ORANGE = 16757504


def build_embed():
    return MessageEmbed()


# Push Events - https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#push-events
def webhook_push(data):
    total_commits = data["total_commits_count"]

    embed = build_embed()
    embed.set_author(name=data["user_username"], icon_url=data["user_avatar"])
    embed.color = COLOR_BLUE
    embed.title = "[{repo}:{branch}] {commit_count} new commit{plural}".format(
        repo=data["repository"]["name"],
        branch=data["ref"].split("/")[-1],
        commit_count=total_commits,
        plural="s" if total_commits > 1 else "",
    )
    embed.url = data["repository"]["git_http_url"]
    embed.timestamp = datetime.utcnow().isoformat()

    embed.description = ""

    for i, commit in enumerate(data["commits"]):
        if i >= 5:
            embed.description += "*...{} more commits not shown*".format(
                total_commits - i
            )
            break

        sha = commit["id"][:7]
        message = commit["message"].split("\n")[0]
        embed.description += "[`{sha}`]({url}) {message} - {author}\n".format(
            sha=sha, url=commit["url"], message=message, author=commit["author"]["name"]
        )

    return embed


# Pipeline Events - https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#pipeline-events
def webhook_pipeline(data):
    embed = build_embed()
    embed.set_author(name=data["user"]["username"], icon_url=data["user"]["avatar_url"])
    status = data["object_attributes"]["status"]
    if status == "failed":
        embed.color = COLOR_RED
    elif status == "success":
        embed.color = COLOR_GREEN
    elif status == "manual":
        embed.color = COLOR_ORANGE

    duration = str(timedelta(seconds=data["object_attributes"]["duration"]))

    embed.title = "[{project}] Pipeline #{pipeline} {status} in {duration}".format(
        project=data["project"]["name"],
        pipeline=data["object_attributes"]["id"],
        status=data["object_attributes"]["status"].upper(),
        duration=duration,
    )
    embed.url = "{}/pipelines/{}".format(
        data["project"]["web_url"], data["object_attributes"]["id"]
    )

    return embed


def send_webhook(embed, url):
    return Webhook.execute_url(url, embeds=[embed])
