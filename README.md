# Washington State Stroke Neurologists Map

An interactive map displaying board-certified stroke neurologists currently practicing in Washington State. Data is automatically updated daily from multiple authoritative sources.

🗺️ **[View Live Map](https://rkalani1.github.io/Wa-stroke/)**

## Features

- **Interactive Map**: Zoom, pan, and click on markers to view detailed provider information
- **Search Functionality**: Search by name, city, hospital, or specialty
- **Real-time Statistics**: See total provider count and last update time
- **Daily Updates**: Automated data refresh every day via GitHub Actions
- **Multiple Data Sources**: Combines data from:
  - CMS NPPES (National Provider Identifier) Database
  - Washington State Department of Health Physician Database
- **Geocoding**: Automatically converts addresses to map coordinates

## Data Sources

### 1. CMS NPPES API
The [National Plan and Provider Enumeration System (NPPES)](https://npiregistry.cms.hhs.gov/) is the authoritative source for National Provider Identifier (NPI) data. We query this API for:
- Neurologists with vascular neurology specialization
- All neurologists in Washington State
- Provider practice locations and contact information

### 2. Washington State Department of Health
The [WA DOH Provider Credential Search](https://fortress.wa.gov/doh/providercredentialsearch/) provides state-level physician licensing data.

## Setup & Deployment

### Prerequisites
- Python 3.11+
- Git
- GitHub account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/rkalani1/Wa-stroke.git
   cd Wa-stroke
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run data collection manually**
   ```bash
   python scripts/update_data.py
   ```

4. **View the map locally**
   Open `index.html` in your web browser or use a local server:
   ```bash
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

### GitHub Pages Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `main`
   - Folder: `/ (root)`
   - Click Save

3. **Wait for deployment**
   - GitHub Actions will build and deploy automatically
   - Your site will be live at: `https://rkalani1.github.io/Wa-stroke/`

### Automated Daily Updates

The GitHub Actions workflow (`.github/workflows/update-data.yml`) automatically:
- Runs daily at 2 AM UTC (6 PM PST / 7 PM PDT)
- Fetches latest data from NPPES and WA DOH
- Updates the `data/neurologists.json` file
- Commits and pushes changes if data has changed
- Can be manually triggered from the Actions tab

## Project Structure

```
Wa-stroke/
├── index.html                      # Main map webpage
├── data/
│   └── neurologists.json          # Provider data (auto-updated)
├── scripts/
│   └── update_data.py             # Data collection script
├── .github/
│   └── workflows/
│       └── update-data.yml        # Daily update automation
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

## Data Format

The `data/neurologists.json` file contains:

```json
{
  "last_updated": "2025-10-26 12:00:00 UTC",
  "total_count": 150,
  "neurologists": [
    {
      "npi": "1234567890",
      "name": "Dr. Jane Smith, MD",
      "credentials": "MD",
      "specialty": "Vascular Neurology",
      "is_vascular_neurology": true,
      "organization": "Seattle Stroke Center",
      "address": "123 Medical Plaza",
      "city": "Seattle",
      "state": "WA",
      "zip": "98101",
      "phone": "206-555-0100",
      "latitude": 47.6062,
      "longitude": -122.3321,
      "source": "NPPES"
    }
  ]
}
```

## Manual Updates

To manually trigger a data update:

1. Go to the **Actions** tab in your GitHub repository
2. Click on "Update Neurologist Data" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for the workflow to complete

## Customization

### Change Update Frequency

Edit `.github/workflows/update-data.yml`:

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 0'    # Weekly on Sunday
```

### Modify Search Criteria

Edit `scripts/update_data.py` to adjust the search terms or filters:

```python
search_terms = [
    "Vascular Neurology",
    "Neurology",
    "Stroke",  # Add more terms
]
```

### Style Customization

The map styling can be customized in `index.html`:
- Colors: Modify the `.header` gradient
- Map height: Adjust `#map { height: 600px }`
- Marker colors: Customize Leaflet marker options

## Troubleshooting

### No data appearing on map
- Check `data/neurologists.json` has entries with valid latitude/longitude
- Verify GitHub Actions workflow ran successfully
- Check browser console for JavaScript errors

### Geocoding failures
- The free Nominatim geocoder has rate limits (1 request/second)
- Some addresses may not geocode properly
- Consider using Google Maps Geocoding API for better results

### GitHub Actions not running
- Verify workflow file is in `.github/workflows/`
- Check repository has Actions enabled in Settings
- Review Actions tab for error logs

## Privacy & Compliance

This map displays publicly available provider information from government databases:
- No patient health information (PHI) is collected or displayed
- All data is sourced from official public registries
- Provider information is already publicly searchable via source databases

## Contributing

To add features or improve data collection:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions or issues, please open a GitHub issue or contact the repository owner.

---

**Disclaimer**: This map is for informational purposes only. Provider information should be verified through official channels. Always confirm provider credentials and availability before seeking medical care.
