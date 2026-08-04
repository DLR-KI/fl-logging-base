---
title: Testing
hide: navigation
---
<!--
SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
SPDX-License-Identifier: CC-BY-4.0
-->

<!-- markdownlint-disable-next-line MD025 -->
# Testing

This projects provides a few different tests and checks.

In general, we have two files which defines all the tests:

- [prek.toml](https://github.com/DLR-KI/fl-logging-base/blob/main/prek.toml)
- CI pipeline like GitHubs [workflows](https://github.com/DLR-KI/fl-logging-base/blob/main/.github/workflows/main.yml)

To easily run these tests locally, use:

```bash
./scripts/test.sh
```

If you only want to run the pre-commit hooks manually, use:

```bash
uv run prek run --all-files
```

Static code checks using [ruff](https://docs.astral.sh/ruff):

```bash
# linter
uv run ruff check src
uv run ruff check scripts
# formatter
uv run ruff format --diff src
uv run ruff format --diff scripts
```

To run automatic static code fixes, use:

```bash
# linter
uv run ruff check --fix src
uv run ruff check --fix tests
uv run ruff check --fix scripts
# formatter
uv run ruff format src
uv run ruff format tests
uv run ruff format scripts
```

Static code analysis using [pylint](https://www.pylint.org/):

```bash
uv run pylint --fail-under=8 src
uv run pylint --exit-zero tests
uv run pylint --exit-zero scripts
```

Static type checks using [ty](https://docs.astral.sh/ty/reference/cli/#ty-check):

```bash
uv run ty src
uv run ty tests
uv run ty scripts
```

General typo checking using [typos](https://github.com/crate-ci/typos):

```bash
uv run typos
```

## Bash Script Checks

```bash
find scripts -type f -name "*.sh" -exec uv run shellcheck --external-sources --shell bash --source-path scripts {} +
```

## Markdown Checks

Verify documentation (markdown) compliance w.r.t. [markdown linting rules](https://github.com/DavidAnson/markdownlint#rules--aliases) further specified inside the [.markdownlint-cli2.jsonc](https://github.com/DLR-KI/fl-logging-base/blob/main/.markdownlint-cli2.jsonc) configuration file.

```bash
npm exec markdownlint-cli2 -- "./docs/**/*.md" "./README.md"
```

## License Checks

```bash
uv run licensecheck
uv run reuse lint
```

## Vulnerability Checks

```bash
uv audit
```

## DependaBot Checks

[dependabot-cli](https://github.com/dependabot/cli) is a tool for testing and debugging Dependabot update jobs.

### Preparations

To run DependaBot checks locally, please ensure that Docker is installed and configured.

Currently, dependabot-cli does not support using rootless Docker directly.
Therefore, we need to build our own DependaBot Docker image and use Docker in Docker.

For system-wide Docker, you can just Download the pre build binaries and from the official [release pages](https://github.com/dependabot/cli/releases).

```Dockerfile
FROM golang:1.26.1-alpine3.23 AS install-dependabot
RUN go install github.com/dependabot/cli/cmd/dependabot@latest \
    && cp $GOPATH/bin/dependabot /usr/local/bin/

FROM docker:29-dind AS runtime
COPY --from=install-dependabot /usr/local/bin/dependabot /usr/local/bin/
ENTRYPOINT ["dependabot"]
```

```bash
docker build -t dependabot-cli:latest .
```

### Run DependaBot Checks

```bash
docker run \
  -it \
  --rm \
  --network=host \
  -v $XDG_RUNTIME_DIR/docker.sock:/var/run/docker.sock \
  -v $HOME/.docker/config.json:/root/.docker/config.json \
  -v .:/repo \
  dependabot-cli update pip test/test --local /repo
```

Note that in the last command line `pip` could be any supported DependaBot manager, depending on what you want to check.
Some useful manager are:

- `pip`
- `uv`
- `pre_commit`
- `github_actions`
- `submodules`
- `docker`
- `docker_compose`
- `devcontainers`

Also take a look at all supported DependaBot managers on [GitHub](https://github.com/dependabot/cli/blob/f27e7af52b72620539c5b371097ca576de5c7fa8/internal/infra/run.go#L270-L300).
Note that this links is referencing to a fixed version.
Check out the main branch too.
