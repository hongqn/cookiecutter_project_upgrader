=============================
Cookiecutter Project Upgrader
=============================


.. image:: https://img.shields.io/pypi/v/cookiecutter_project_upgrader.svg
        :target: https://pypi.python.org/pypi/cookiecutter_project_upgrader

.. image:: https://img.shields.io/travis/thomasjahoda/cookiecutter_project_upgrader.svg
        :target: https://travis-ci.org/thomasjahoda/cookiecutter_project_upgrader

.. image:: https://readthedocs.org/projects/cookiecutter-project-upgrader/badge/?version=latest
        :target: https://cookiecutter-project-upgrader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




upgrade projects created from a Cookiecutter template


* Free software: MIT license
* Documentation: https://cookiecutter-project-upgrader.readthedocs.io.

Features
--------

Cookiecutter Project Upgrader allows for the update of projects that are created using cookiecutter.
When run the first time on a project, it creates a new branch that contains the latest cookiecuttered code,
using a JSON file with context that matches the existing service.
This file can be created through cookiecutter with the following contents:

`{{ cookiecutter | jsonify }}`

The script uses the [Click](https://github.com/pallets/click) framework.

```
Usage: cookiecutter_project_upgrader [OPTIONS]

  Upgrade projects created from a Cookiecutter template

Options:
  -c, --context-file PATH  Default: docs/cookiecutter_input.json
  -b, --branch TEXT        Default: cookiecutter-template
  -m, --merge-now          Execute a git merge after a successful update
  --help                   Show this message and exit.
```

Note that you will need a recent version of git for this to work. (it needs --no-checkout on git worktree)


Auto-Completion
---------------
Because the script uses Click, you can enable completion for Zsh and Bash.

For Bash, add the following to your `.bashrc` or some other profile initialization file.
`eval "$(_COOKIECUTTER_PROJECT_UPGRADER_COMPLETE=source cookiecutter_project_upgrader)"`

For Zsh, please read [the Click documentation](https://click.palletsprojects.com/en/7.x/bashcomplete/#activation).

Credits
-------

The concept and some code is heavily based on https://github.com/senseyeio/cupper, with some changes
to use Click and some flags and default values to ease usage. Also cleanup has been done and automated tests have been added.

This package was created with Cookiecutter_ and the `thomasjahoda/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/thomasjahoda/cookiecutter
.. _`thomasjahoda/cookiecutter-pypackage`: https://github.com/thomasjahoda/cookiecutter-pypackage
