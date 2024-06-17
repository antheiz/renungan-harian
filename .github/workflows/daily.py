name: Scrape and Update README

on:
  # schedule:
    # - cron: '0 5 * * *'  # Menjalankan setiap hari pada pukul 5 pagi
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository content
        uses: actions/checkout@v4 # Checkout the repository content to github runner.

      - name: Setup Python Version
        uses: actions/setup-python@v5
        with:
          python-version: 3.8 # Install the python version needed

      - name: Install Python dependencies
        run: python -m pip install --upgrade pip requests beautifulsoup4

      - name: Execute Python script # Run the run.py to get the latest data
        run: python main.py

      - name: Check if there are any changes
        id: verify_diff
        run: |
          git diff --quiet . || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Commit
        if: steps.verify_diff.outputs.changed == 'true'
        run: |
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add 
          git commit -m "Build" -a

      - name: Push
        if: steps.verify_diff.outputs.changed == 'true'
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GH_TOKEN }}
          branch: ${{ github.ref }}
