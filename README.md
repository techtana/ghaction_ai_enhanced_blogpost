# AI Enhanced Blog Post GitHub Action

[![Test](https://github.com/techtana/ghaction_ai_enhanced_blogpost/actions/workflows/test.yml/badge.svg)](https://github.com/techtana/ghaction_ai_enhanced_blogpost/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/techtana/ghaction_ai_enhanced_blogpost)
![GitHub last commit](https://img.shields.io/github/last-commit/techtana/ghaction_ai_enhanced_blogpost)
![GitHub top language](https://img.shields.io/github/languages/top/techtana/ghaction_ai_enhanced_blogpost)

This GitHub Action automates the enhancement of Jekyll blog posts using OpenAI's API. It processes markdown files from a `_posts_commit` directory, enhances them based on a flexible policy system, and moves them to the `_posts` directory, ready for publishing.

## Features

-   **AI-Powered Content Enhancement**: Leverages OpenAI's Chat Completions API to improve your blog posts.
-   **Flexible Enhancement Policies**: Define enhancement instructions directly in the post's front matter or in separate policy files.
-   **Boilerplate Instructions**: Prepends a default set of instructions to every API call for consistent results.
-   **Category-Based File Routing**: Automatically organizes enhanced posts into subdirectories based on the `categories` front matter.
-   **Idempotent**: Skips posts that have already been enhanced.
-   **Configurable**: Key settings like the boilerplate path can be configured in `config.py`.

## How it Works

The action performs the following steps for each markdown file in the `_posts_commit` directory:

1.  **Moves Processed Files**: All files are moved from `_posts_commit` to `_posts`. If a `categories` field is present in the front matter, the file is moved to `_posts/<category>`.
2.  **Skips Already Enhanced Posts**: If a post already contains a `{% comment %}` block (indicating a previous enhancement), it is moved without being re-processed.
3.  **Skips Posts Without a Policy**: If a post does not have an `enhance_policy` in its front matter, or if the policy is empty, the post is moved without AI enhancement.
4.  **Applies AI Enhancement**:
    -   It looks for an `enhance_policy` in the post's front matter.
    -   If the policy value corresponds to a file in the `_enhance_policy` directory, the content of that file is used as the instruction.
    -   Otherwise, the policy value itself is used as the instruction.
    -   A boilerplate instruction from `_prompts/default_boilerplate.prompt` is prepended to the policy.
    -   The combined instruction and the post's content are sent to the OpenAI API.
5.  **Preserves Original Content**: The original content of the post is preserved within a `{% comment %}` block after the new, AI-generated content.

## Usage

This action is designed to be used in a GitHub Actions workflow.

```yaml
- name: Enhance Posts
  uses: techtana/ghaction_ai_enhanced_blogpost@main
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

-   `openai_api_key` (required): Your OpenAI API key. This should be stored as a secret in your repository.
-   `github_token` (required): The GitHub token. You should use the default `${{ secrets.GITHUB_TOKEN }}`.

### Example Workflow

```yaml
name: Enhance and Deploy Blog Posts

on:
  push:
    branches:
      - main

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Enhance Posts
        uses: techtana/ghaction_ai_enhanced_blogpost@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}

      - name: Commit Changes
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add .
          git commit -m "Enhance posts" || echo "No changes to commit"
          git push

      # ... further steps to build and deploy your Jekyll site
```

### Example Jekyll Posts

**Using a policy from a file:**

```markdown
---
layout: post
title: "Post with a Policy File"
categories: [tech]
enhance_policy: "summarize_for_techies.txt"
---

This is the original content...
```

**Using a policy from the front matter:**

```markdown
---
layout: post
title: "Post with a Policy String"
enhance_policy: "Summarize this post in three paragraphs."
---

This is the original content...
```

## Configuration

-   **Boilerplate**: The default boilerplate instruction is located at `_prompts/default_boilerplate.prompt`. You can modify this file to change the default instructions for the AI.
-   **Configuration File**: The path to the boilerplate file is defined in `config.py`.

## Development

This action is composed of a Python script (`main.py`) that uses the `openai` and `python-frontmatter` libraries. The dependencies are listed in `requirements.txt`. The action is defined in `action.yml`.