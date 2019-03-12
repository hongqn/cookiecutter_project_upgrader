import json
import os
import pytest
import subprocess
from contextlib import contextmanager
from pathlib import Path
from pytest_cookies import Cookies, Result

from cupper.logic import update_project_template_branch
from tests.files import copy_children
from tests.tmp_files import CreateTempDirectory

SAMPLE_CONTEXT = {
    "full_name": "Bernd Huber",
    "project_name": "My Project",
    "project_slug": "my_project",
    "version": "0.1.0"
}


@pytest.fixture()
def empty_git_repository():
    with CreateTempDirectory("some_git_repository") as git_repo:
        subprocess.run(["git", "init"], cwd=str(git_repo), check=True)
        yield git_repo


@pytest.fixture()
def git_repository_with_a_file_and_commit(empty_git_repository: Path):
    empty_git_repository.joinpath("README.rst").write_text("initial text from a git repo", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=str(empty_git_repository), check=True)
    subprocess.run(["git", "commit", "-m", "initial (README.rst)"], cwd=str(empty_git_repository), check=True)
    return empty_git_repository


@pytest.fixture()
def cookiecutter_template_directory(empty_git_repository: Path):
    dummy_template_directory = Path(__file__).parent.joinpath("dummy_cookiecutter_template")
    copy_children(dummy_template_directory, empty_git_repository)
    subprocess.run(["git", "add", "-A"], cwd=str(empty_git_repository), check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=str(empty_git_repository), check=True)
    return empty_git_repository


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def test_initial_cupper_without_change_on_template_just_initializes_branch(cookiecutter_template_directory: Path,
                                                                           cookies: Cookies):
    result: Result = cookies.bake(extra_context=SAMPLE_CONTEXT, template=str(cookiecutter_template_directory))
    if result.exception is not None:
        raise result.exception
    project_directory = Path(result.project)
    subprocess.run(["git", "init"], cwd=str(project_directory), check=True)
    subprocess.run(["git", "add", "-A"], cwd=str(project_directory), check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=str(project_directory), check=True)

    context = json.loads(project_directory.joinpath("docs", "cookiecutter_input.json").read_text(encoding="utf-8"))
    update_project_template_branch(context, str(project_directory), "cookiecutter-template")
    subprocess.run(["git", "rev-parse", "cookiecutter-template"], cwd=str(project_directory), check=True)


def test_first_run_creates_branch_on_first_commit_and_updates_based_on_template(cookiecutter_template_directory: Path,
                                                                                cookies: Cookies):
    result: Result = cookies.bake(extra_context=SAMPLE_CONTEXT, template=str(cookiecutter_template_directory))
    if result.exception is not None:
        raise result.exception
    project_directory = Path(result.project)
    subprocess.run(["git", "init"], cwd=str(project_directory), check=True)
    subprocess.run(["git", "add", "-A"], cwd=str(project_directory), check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=str(project_directory), check=True)

    context = json.loads(project_directory.joinpath("docs", "cookiecutter_input.json").read_text(encoding="utf-8"))

    cookiecutter_template_directory.joinpath("{{cookiecutter.project_slug}}", "README.rst").write_text("updated readme")
    subprocess.run(["git", "add", "-A"], cwd=str(cookiecutter_template_directory), check=True)
    subprocess.run(["git", "commit", "-m", "updated readme"], cwd=str(cookiecutter_template_directory), check=True)

    context['_template'] = str(cookiecutter_template_directory)
    update_project_template_branch(context, str(project_directory), "cookiecutter-template")

    subprocess.run(["git", "merge", "cookiecutter-template"], cwd=str(project_directory), check=True)
    readme = project_directory.joinpath("README.rst").read_text(encoding="utf-8")
    assert readme == "updated readme"