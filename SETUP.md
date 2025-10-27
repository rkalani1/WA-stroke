# Setup Instructions

## ✅ What's Already Done

Your Washington State Stroke Neurologist Map is almost ready! Here's what has been created:

- ✅ Interactive map webpage (`index.html`)
- ✅ Python data collection script (`scripts/update_data.py`)
- ✅ GitHub repository created and pushed to: https://github.com/rkalani1/WA-stroke
- ✅ Documentation (`README.md`)
- ✅ GitHub Actions workflow file (`.github/workflows/update-data.yml`) - needs to be added

## 🚀 Next Steps to Complete Deployment

### Step 1: Enable GitHub Pages

1. Go to your repository: https://github.com/rkalani1/WA-stroke
2. Click on **Settings** (top navigation)
3. In the left sidebar, click **Pages**
4. Under "Source":
   - Select: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **Save**
6. Wait 1-2 minutes for deployment
7. Your map will be live at: **https://rkalani1.github.io/WA-stroke/**

### Step 2: Add the GitHub Actions Workflow (for Daily Auto-Updates)

The workflow file couldn't be pushed automatically due to GitHub token permissions. You have two options:

#### Option A: Add Workflow File Through GitHub Web Interface (Easiest)

1. Go to: https://github.com/rkalani1/WA-stroke
2. Click **Add file** → **Create new file**
3. Name the file: `.github/workflows/update-data.yml`
4. Copy the content from your local file at: `/Users/rizwankalani/Wa-stroke/.github/workflows/update-data.yml`
5. Or copy this content:

```yaml
name: Update Neurologist Data

on:
  # Run daily at 2 AM UTC (6 PM PST / 7 PM PDT)
  schedule:
    - cron: '0 2 * * *'

  # Allow manual trigger
  workflow_dispatch:

jobs:
  update-data:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run data collection script
        run: |
          python scripts/update_data.py

      - name: Check for changes
        id: check_changes
        run: |
          git diff --quiet data/neurologists.json || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Commit and push if changed
        if: steps.check_changes.outputs.changed == 'true'
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add data/neurologists.json
          git commit -m "Update neurologist data - $(date +'%Y-%m-%d')"
          git push

      - name: No changes detected
        if: steps.check_changes.outputs.changed != 'true'
        run: echo "No changes to neurologist data"
```

6. Click **Commit changes** → **Commit directly to the main branch**

#### Option B: Re-authenticate GitHub CLI with Workflow Permissions

From your terminal:

```bash
# Re-authenticate with workflow scope
gh auth login -s workflow

# Then push the workflow file
cd /Users/rizwankalani/Wa-stroke
git commit -m "Add GitHub Actions workflow for daily updates"
git push
```

### Step 3: Manually Run First Data Collection

To populate your map with initial data:

1. Go to: https://github.com/rkalani1/WA-stroke/actions
2. Click on **"Update Neurologist Data"** workflow
3. Click **"Run workflow"** dropdown
4. Click **"Run workflow"** button
5. Wait for the workflow to complete (2-5 minutes)
6. Check the Actions tab to monitor progress

**OR** run locally:

```bash
cd /Users/rizwankalani/Wa-stroke
pip install -r requirements.txt
python scripts/update_data.py
git add data/neurologists.json
git commit -m "Initial data collection"
git push
```

### Step 4: Verify Your Deployment

1. Visit your live map: **https://rkalani1.github.io/WA-stroke/**
2. Verify the map loads and displays markers
3. Test the search functionality
4. Check the "Last Updated" timestamp

## 🔄 Ongoing Updates

Once set up, the system will automatically:
- Run daily at 2 AM UTC (6 PM PST / 7 PM PDT)
- Fetch the latest neurologist data from NPPES
- Update the map if any changes are found
- Commit and push changes automatically

You can also manually trigger updates anytime from the **Actions** tab.

## 🛠️ Customization Options

### Change Update Frequency

Edit the workflow file's cron schedule:
- Daily: `'0 2 * * *'` (current)
- Every 6 hours: `'0 */6 * * *'`
- Weekly: `'0 0 * * 0'` (Sundays)

### Add More Data Sources

Edit `scripts/update_data.py` to:
- Add custom search terms
- Integrate additional databases
- Implement WA DOH web scraping

### Customize Map Appearance

Edit `index.html` to:
- Change color scheme
- Adjust map center/zoom
- Modify popup content
- Add additional filters

## 📞 Troubleshooting

### Map Not Loading
- Check GitHub Pages is enabled
- Verify deployment completed (Settings → Pages)
- Wait 2-3 minutes after enabling Pages

### No Markers on Map
- Run the data collection workflow
- Check `data/neurologists.json` has entries
- Verify geocoding succeeded (latitude/longitude present)

### Workflow Not Running
- Verify workflow file exists at `.github/workflows/update-data.yml`
- Check Actions are enabled (Settings → Actions → Allow all actions)
- Review workflow logs in Actions tab for errors

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Leaflet.js Documentation](https://leafletjs.com/reference.html)
- [NPPES API Documentation](https://npiregistry.cms.hhs.gov/api-page)

---

**Need Help?** Open an issue at: https://github.com/rkalani1/WA-stroke/issues
