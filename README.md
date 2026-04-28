# PMA Experiment Suite

This repository contains the code used for the thesis experiments built around the PMA framework.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Each experiment reads model credentials from environment variables. Use the matching `.env.example` in the experiment directory as the template for the variables you need, then export those variables in your shell before running the experiment.

Example:

```bash
cd Brain_Helplessness
cp .env.example .env
# Fill .env, then export the values before running.
set -a
source .env
set +a
python main.py
```

## Projects

- `Brain_Helplessness`: learned helplessness experiment
- `Brain_CognitiveDiss`: cognitive dissonance experiment
- `Brain_Threshold`: foot-in-the-door experiment and door-in-the-face extension
- `Brain_Cyberball`: Cyberball ostracism experiment and bystander-conformity extension
- `Brain_DiffResponsibility`: diffusion of responsibility experiment and social-role extension
- `Brain_town`: 8-agent daily life simulation in a small town
- `绘图`: plotting scripts for thesis figures

Each project is self-contained and includes its own:
- `main.py` entry point
- experiment runner
- prompt templates
- model router
- PMA motivation layer

## Dependencies

The shared Python dependencies are listed in `requirements.txt`:

- `openai` for OpenAI-compatible model providers
- `numpy`, `scikit-learn` for analysis and similarity calculations
- `matplotlib` for plotting thesis figures

## Models

The projects are configured to use these model names:
- `Llama-3-70B-Instruct`
- `Qwen3.5-35B-A3B`
- `DeepSeek-V3.2`
- `GLM-4.5-Air`

Each project includes its own `.env.example` describing the required API keys.

## GitHub Upload Checklist

```bash
git init
git add .
git status
git commit -m "Initial thesis experiment suite"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Notes

- The directory `心理学实验论文/` is local supporting material and is excluded from version control by the root `.gitignore`.
- The `绘图/` directory is included as plotting code; generated image outputs are ignored.
- Runtime outputs such as `*.db`, `*.log`, caches, and local IDE files are also excluded.
- If you want to run one experiment, enter that project directory and run its `main.py`.
