import json
import requests
import sys

from git import exc, Remote, Repo

BASE_REPO_NAME = "TEAM-"
NUMBER_OF_TEAMS = 60
ORGANIZATION = "Reality-Hack-2022"
with open("personal_access_token", "r") as f:
    ACCESS_TOKEN = f.read().strip()


def create_remote_repository(team_name):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {ACCESS_TOKEN}"
    }
    data = {"name": team_name}
    request = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION}/repos",
        data=json.dumps(data),
        headers=headers
    )
    pass


def add_repository_remote(repo, team_name):
    Remote.create(
        repo, team_name,
        f"https://{ACCESS_TOKEN}@github.com/{ORGANIZATION}/{team_name}.git"
    )


def push_repository(repo, team_name):
    remote = repo.remotes[team_name]
    remote.push("main")


def remove_repository_remote(repo, team_name):
    Remote.remove(repo, team_name)


def delete_remote_repository(team_name):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {ACCESS_TOKEN}"
    }
    request = requests.delete(
        f"https://api.github.com/repos/{ORGANIZATION}/{team_name}",
        headers=headers
    )


if __name__ == "__main__":
    repo = Repo("../../reality-hack-2022-repo")
    for n in range(NUMBER_OF_TEAMS):
        team_name = str(n + 1)
        if len(team_name) == 1:
            team_name = f"0{team_name}"
        team_name = f"{BASE_REPO_NAME}{team_name}"
        if len(sys.argv) > 1:
            if "delete" in sys.argv[1].lower():
                delete_remote_repository(team_name)
                try:
                    remove_repository_remote(repo, team_name)
                except exc.GitCommandError as error:
                    print(error)
            else:
                print("What are you even trying to do, here?")
                sys.exit(1)
        else:  # create
            create_remote_repository(team_name)
            add_repository_remote(repo, team_name)
            push_repository(repo, team_name)
