======
Cupper
======


.. image:: https://img.shields.io/pypi/v/cupper.svg
        :target: https://pypi.python.org/pypi/cupper

.. image:: https://img.shields.io/travis/thomasjahoda/cupper.svg
        :target: https://travis-ci.org/thomasjahoda/cupper

.. image:: https://readthedocs.org/projects/cupper/badge/?version=latest
        :target: https://cupper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Cookiecutter Upper - upgrade projects created from a template


* Free software: MIT license
* Documentation: https://cupper.readthedocs.io.

Features
--------

Cupper allows for the update of services that are created using cookiecutter.
When run, it creates a new branch that contains the latest cookiecuttered code,
using a JSON file with context that matches the existing service.
This file can be created through cookiecutter with the following contents:

`{{ cookiecutter | jsonify }}`

The script takes two arguments: a JSON file containing configuration for cookiecutter, and the name of the branch to create.

`cupper .cookiecutter.json template`

You can then merge these changes into your existing code:

`git merge template`

This code is heavily based on https://github.com/aroig/cookiecutter-latex-paper/blob/master/make/cookiecutter-update.py, with a few very small changes.

Note that you will need a recent version of git for this to work (it needs --no-checkout on git worktree)

Credits
-------

This package was created with Cookiecutter_ and the `thomasjahoda/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/thomasjahoda/cookiecutter
.. _`thomasjahoda/cookiecutter-pypackage`: https://github.com/thomasjahoda/cookiecutter-pypackage
