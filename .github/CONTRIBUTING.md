# Contributing

Thank you for your interest in contributing to this project.

## Before You Start

- Check existing issues and discussions before opening a new one.
- For bug reports, include clear reproduction steps and expected behavior.
- For feature requests, describe the problem the change would solve.

## Development

The project uses [uv](https://uv.dev) package manager.

If you don't have it installed, you can install it by following the instructions in the [uv documentation](https://uv.dev/docs/installation).
Or you can use the following commands to install it directly.

<details>

<summary>Download for windows</summary>

### Windows(PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```
> **Note for Windows Users:** If PowerShell shows `uv : The term 'uv' is not recognized`, restart your terminal session or refresh your environment variables so the global `uv` binary path is loaded into `PATH`.

</details>

<details>

<summary>Download for Linux / macOS</summary>

### Linux / macOS

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
</details>

---

- Fork the repository.
```bash
git clone https://github.com/Noor-Taquee/Physics-Simulation.git
cd Physics-Simulation
```

- Create a branch for your change.
```bash
git checkout main
git pull origin main
git checkout -b <your-username>/<your-branch-name>
```

- Install dependencies
```bash
uv sync
```

- Make your changes.

- Test your work locally.

- Format and lint your code before committing.

```bash
uv run ruff format
uv run ruff check
```

- Open a pull request with a clear description of the change.


## Pull Requests

Please make sure your pull request:

- Has a clear title and description
- Explains the purpose of the change
- Includes testing notes where relevant
- Links related issues when applicable

## Code of Conduct

By participating in this project, you agree to follow the guidelines in [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).
