"""Create the release notes."""
import re
import sys
from datetime import datetime

from github import Github

REPOSITORY = sys.argv[8]

BODY = """[![Downloads for this release](https://img.shields.io/github/downloads/{repository}/{version}/total.svg)](https://github.com/{repository}/releases/{version})

{changes}

"""

CHANGES_BREAKING = "### 💥 Breaking Changes"
CHANGES_ENHANCEMENTS = "### ✨ Enhancements"
CHANGES_FIXES = "### 🐛 Fixes"
CHANGES_MAINTENANCE = "### 🔨 Maintenance"
CHANGES_DOCUMENTATION = "### 📚 Documentation"
CHANGES_OTHER = "### Other"

CHANGE = "- [{line}]({link}) - @{author}\n"
NOCHANGE = "_No changes in this release._"

GITHUB = Github(sys.argv[2])


def _new_commits(repo, sha):
    """Get new commits in repo."""

    dateformat = "%a, %d %b %Y %H:%M:%S GMT"
    release_commit = repo.get_commit(sha)
    since = datetime.strptime(release_commit.last_modified, dateformat)
    commits = repo.get_commits(since=since)
    return False if len(list(commits)) == 1 else reversed(list(commits)[:-1])


def _last_repo_release(github, skip=True):
    """Return last release."""
    repo = github.get_repo(REPOSITORY)
    tag_sha = None
    if tags := list(repo.get_tags()):
        reg = "(v|^)?(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)(b\\d+)?$"
        for tag in tags:
            tag_name = tag.name
            if re.match(reg, tag_name):
                tag_sha = tag.commit.sha
                if skip:
                    skip = False
                    continue
                break
    return {"tag_name": tag_name, "tag_sha": tag_sha}


def _process_chunks(change_title, changes):
    return change_title + "\n" + changes + "\n" if changes else ""


def _add_line(startswith, commit, msg):
    if "Merge branch " in msg:
        return
    if "Merge pull request " in msg:
        return
    if "\n" in msg:
        msg = msg.split("\n")[0]
    try:
        author = commit.author.login if commit.author else None
    except Exception:  # pylint: disable=broad-exception-caught
        author = None
    if msg.startswith(startswith):
        msg = msg[len(startswith) :].strip()
    return CHANGE.format(line=msg, link=commit.html_url, author=author)


def _get_repo_commits(github, skip=True):
    changes = ""
    repo_changes_breaking = ""
    repo_changes_enhancement = ""
    repo_changes_fixes = ""
    repo_changes_maintenance = ""
    repo_changes_documentation = ""
    repo_changes_other = ""
    repo = github.get_repo(REPOSITORY)
    if commits := _new_commits(repo, _last_repo_release(github, skip)["tag_sha"]):
        for commit in commits:
            msg = repo.get_git_commit(commit.sha).message
            if msg.startswith("break:"):
                repo_changes_breaking += _add_line("break:", commit, msg)
            elif msg.startswith("feat:"):
                repo_changes_enhancement += _add_line("feat:", commit, msg)
            elif msg.startswith("fix:"):
                repo_changes_fixes += _add_line("fix:", commit, msg)
            elif msg.startswith("maint:"):
                repo_changes_maintenance += _add_line("maint:", commit, msg)
            elif msg.startswith("doc:"):
                repo_changes_documentation += _add_line("doc:", commit, msg)
            elif other := _add_line("", commit, msg):
                repo_changes_other += other

        changes += _process_chunks(CHANGES_BREAKING, repo_changes_breaking)
        changes += _process_chunks(CHANGES_ENHANCEMENTS, repo_changes_enhancement)
        changes += _process_chunks(CHANGES_FIXES, repo_changes_fixes)
        changes += _process_chunks(CHANGES_MAINTENANCE, repo_changes_maintenance)
        changes += _process_chunks(CHANGES_DOCUMENTATION, repo_changes_documentation)
        changes += _process_chunks(CHANGES_OTHER, repo_changes_other)
    else:
        changes = NOCHANGE
    return changes


# Update release notes:
UPDATERELEASE = str(sys.argv[4])
REPO = GITHUB.get_repo(REPOSITORY)
if UPDATERELEASE == "yes":
    VERSION = str(sys.argv[6]).replace("refs/tags/", "")
    RELEASE = REPO.get_release(VERSION)
    RELEASE.update_release(
        name=VERSION,
        message=BODY.format(
            version=VERSION,
            changes=_get_repo_commits(GITHUB),
            repository=REPOSITORY,
        ),
        prerelease=True,
    )
else:
    repo_changes = _get_repo_commits(GITHUB, False)  # pylint: disable=invalid-name
    if repo_changes != NOCHANGE:
        VERSION = _last_repo_release(GITHUB, False)["tag_name"]
        VERSION = f"{VERSION[:-1]}{int(VERSION[-1])+1}"
        REPO.create_issue(
            title=f"Create release {VERSION}?",
            labels=["New release"],
            assignee=sys.argv[10],
            body=repo_changes,
        )
    else:
        print("Not enough changes for a release.")
