# -*- coding: utf-8 -*-

import sys

import json
import os
import shutil
import subprocess
from cookiecutter.main import cookiecutter


class TemporaryWorkdir:
    """Context Manager for a temporary working directory of a branch in a git repo"""

    def __init__(self, path, repo, branch='master'):
        self.repo = repo
        self.path = path
        self.branch = branch

    def __enter__(self):
        if not os.path.exists(os.path.join(self.repo, ".git")):
            raise Exception("Not a git repository: %s" % self.repo)

        if os.path.exists(self.path):
            raise Exception("Temporary directory already exists: %s" % self.path)

        os.makedirs(self.path)
        subprocess.run(["git", "worktree", "add", "--no-checkout", self.path, self.branch],
                       cwd=self.repo)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
        subprocess.run(["git", "worktree", "prune"], cwd=self.repo)


def update_template(context, project_directory, branch):
    """Update template branch from a template url"""
    template_url = context['_template']
    tmpdir = os.path.join(project_directory, ".git", "cookiecutter")
    project_slug = os.path.basename(project_directory)
    tmp_workdir = os.path.join(tmpdir, project_slug)

    context['project_slug'] = project_slug
    # create a template branch if necessary
    if subprocess.run(["git", "rev-parse", "-q", "--verify", branch], cwd=project_directory).returncode != 0:
        print(f"Creating git branch {branch}")
        firstref = subprocess.run(["git", "rev-list", "--max-parents=0", "--max-count=1", "HEAD"],
                                  cwd=project_directory,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True,
                                  check=True).stdout.strip()
        subprocess.run(["git", "branch", branch, firstref])

    with TemporaryWorkdir(tmp_workdir, repo=project_directory, branch=branch):
        # update the template
        print(f"Updating template in branch {branch} using extra_context={context}")
        cookiecutter(template_url,
                     no_input=True,
                     extra_context=context,
                     overwrite_if_exists=True,
                     output_dir=tmpdir)

        # commit to template branch
        subprocess.run(["git", "add", "-A", "."], cwd=tmp_workdir, check=True)
        subprocess.run(["git", "commit", "-m", "Update template"],
                       cwd=tmp_workdir, check=True)
        subprocess.run(["git", "push", "origin", branch],
                       cwd=tmp_workdir, check=False)

        print(f"===========")
        print(f"Changes have been commited into branch '{branch}'. Use the following command to update your branch:\n"
              f"git merge {branch}")


def main():
    if not 1 <= len(sys.argv) <= 3:
        _help_text()
        sys.exit(1)
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--help":
            _help_text()
            sys.exit(0)

    if len(sys.argv) == 3:
        branch = sys.argv[2]
    else:
        branch = "cookiecutter-template"

    if len(sys.argv) >= 2:
        context_file = sys.argv[1]
    else:
        context_file = "docs/cookiecutter_input.json"
    with open(context_file, 'r') as fd:
        context = json.load(fd)

    project_directory = os.getcwd()
    update_template(context, project_directory, branch=branch)


def _help_text():
    print("Usage: cupper [context-filename:docs/cookiecutter_input.json] [branch:cookiecutter-template]")
