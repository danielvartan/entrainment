# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

Please note that this package is released with a [Contributor Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By contributing to this project, you agree to abide by its terms.

## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at
[https://github.com/giperbio/entrainment/issues](https://github.com/giperbio/entrainment/issues).

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in as much detail as you can.
  Questions to start a discussion about the issue are welcome.

### Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "please-help" is open to whoever wants to implement it.

Please do not combine multiple feature enhancements into a single pull request.

Note: this project is very conservative, so new features that aren't tagged with "please-help" might not get into core.
We're trying to keep the code base small, extensible, and streamlined.
Whenever possible, it's best to try and implement feature ideas as separate projects outside of the core codebase.

### Write Documentation

`entrainment` could always use more documentation, whether as part of the official `entrainment` docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at [https://github.com/giperbio/entrainment/issues](https://github.com/giperbio/entrainment/issues).

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Setting Up the Code for Local Development

Here's how to set up `entrainment` for local development.

1. Fork the `entrainment` repo on GitHub.
2. Clone your fork locally:

   ```bash
   git clone git@github.com:your_name_here/entrainment.git
   ```

3. Install your local copy into a virtualenv.
   Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

   ```bash
   cd entrainment/
   pip install -e .
   ```

4. Create a branch for local development:

   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and lint check:

6. Ensure that your feature or commit is fully covered by tests.

7. Commit your changes and push your branch to GitHub:

   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

8. Submit a pull request through the GitHub website.

## Contributor Guidelines

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request should be contained:
   if it's too big consider splitting it into smaller pull requests.
3. If the pull request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
4. The pull request must pass all CI/CD jobs before being ready for review.
5. If one CI/CD job is failing for unrelated reasons you may want to create another PR to fix that first.

### Coding Standards

All `entrainment` code must follow the [PEP 8 Style Guide](https://peps.python.org/pep-0008/).

## Acknowledgments

This contributing guide was based on the [`cookiecutter` contributing guide](https://github.com/cookiecutter/cookiecutter/blob/main/CONTRIBUTING.md).
