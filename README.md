# 📚 aideml - Citation Tracker

An automated citation tracking website that monitors and displays papers citing our research. The site automatically updates using GitHub Actions and provides a beautiful, modern interface for viewing citation data.

## 🌟 Features

- **Automated Citation Tracking**: Uses SerpAPI to search Google Scholar for citing papers
- **Beautiful Web Interface**: Modern, responsive design with interactive charts
- **Real-time Statistics**: Total citations, recent citations, H-index, and trends
- **GitHub Actions Integration**: Automatically updates daily
- **Cloudflare Workers Deployment**: Fast, serverless deployment on the edge
- **Mobile Responsive**: Works perfectly on all devices
- **Error Handling**: Graceful fallback when API is unavailable

## 🚀 Live Demo

The website is automatically deployed on **Cloudflare** and updated daily via GitHub Actions. Every time the citation data is updated, the site is automatically redeployed with the latest information.

## 📋 Setup Instructions

### 1. Fork/Clone this Repository

```bash
git clone https://github.com/yourusername/yanhua.ai.git
cd yanhua.ai
```

### 2. Get a SerpAPI Key

1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for a free account (100 searches/month free)
3. Get your API key from the dashboard

### 3. Configure API Key and Cloudflare Credentials

You will need to configure secrets for both SerpAPI and Cloudflare to enable automated updates and deployment.

**GitHub Secrets (required for automation)**
1. Go to your repository's **Settings** tab
2. Navigate to **Secrets and variables** → **Actions**
3. Add the following new secrets:
   - `SERPAPI_KEY`: Your SerpAPI key.
   - `CLOUDFLARE_API_TOKEN`: An API token with "Worker KV Storage" write permissions.
   - `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID.
   - `CLOUDFLARE_KV_NAMESPACE_ID`: The ID of the KV namespace you created.

### 4. Deploy on Cloudflare

1. **Install Wrangler CLI**:
   ```bash
   npm install -g wrangler
   ```
2. **Authenticate Wrangler**:
   ```bash
   wrangler login
   ```
3. **Create a KV Namespace**:
   - Go to your Cloudflare dashboard.
   - Navigate to **Workers & Pages** -> **KV**.
   - Click **Create a namespace** and give it a name (e.g., `CITATIONS_KV`).
   - Copy the **ID** of the newly created namespace.
4. **Update `wrangler.toml`**:
   - Open the `wrangler.toml` file in the project root.
   - Replace `YOUR_KV_NAMESPACE_ID` with the actual ID you copied.
5. **Deploy the Worker**:
   ```bash
   wrangler deploy
   ```
   Your site will be live at the URL provided by Wrangler.

### 5. Customize for Your Paper (Optional)

If you want to track a different arXiv paper:

1. Edit `fetch_citations.py`
2. Change the `target_paper_url` in the `CitationTracker` initialization
3. Update the paper reference in `index.html`

## 🔄 How It Works

### Automatic Updates

The system runs automatically daily using GitHub Actions:

1. **Fetch Citations**: Uses SerpAPI to search Google Scholar for papers citing your research.
2. **Process Data**: Extracts paper information and calculates statistics.
3. **Update KV Store**: Saves the new data directly to the Cloudflare KV namespace using Wrangler.
4. **Deploy**: The Cloudflare Worker automatically serves the latest data from the KV store.

### Manual Updates

You can manually trigger an update:

1. Go to the **Actions** tab in your repository.
2. Select the **Update Citations** workflow.
3. Click **Run workflow**.

## 📁 Project Structure

```
├── index.html              # Main website file
├── worker.js               # Cloudflare Worker script
├── wrangler.toml           # Cloudflare configuration
├── fetch_citations.py      # Citation tracking script
├── citations_data.json     # Local data file (auto-generated)
├── requirements.txt        # Python dependencies
├── .github/workflows/
│   └── update-citations.yml # GitHub Actions workflow
└── README.md               # This file
```

## 🛠 Technical Details

### Dependencies

- **Python 3.9+**
- **requests**: For API calls
- **python-dotenv**: For loading .env files
- **SerpAPI**: For Google Scholar access
- **Cloudflare Wrangler**: For deployment and KV updates
- **Chart.js**: For data visualization
- **GitHub Actions**: For automation

### API Usage

The script searches Google Scholar using patterns like:
- `arxiv:2502.13138` - Direct arXiv ID search
- Papers that cite the target paper

### Data Structure

The data is stored in Cloudflare KV as a JSON string with the key `citations_data`. The structure is:

```json
{
  "last_updated": "2025-01-27 10:00:00 UTC",
  "target_paper": "https://arxiv.org/abs/2502.13138",
  "total_citations": 15,
  "recent_citations": 3,
  "avg_citations_per_month": 2.5,
  "h_index": 4,
  "timeline": [...],
  "papers": [...]
}
```

## 🎨 Customization

### Styling

The website uses modern CSS with:
- Gradient backgrounds
- Glass-morphism effects
- Smooth animations
- Responsive grid layout

### Colors and Themes

Edit the CSS variables in `index.html` to customize:
- Primary colors: `#3498db`, `#2980b9`
- Background: Gradient from `#667eea` to `#764ba2`
- Card backgrounds: `rgba(255, 255, 255, 0.95)`

### Update Frequency

Change the cron schedule in `.github/workflows/update-citations.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'     # Daily at midnight (current setting)
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 */12 * * *' # Every 12 hours
```

## 📊 Statistics Explained

- **Total Citations**: Number of papers found citing your work
- **Recent Citations**: Papers published in the last 30 days
- **Avg. Citations/Month**: Average rate of new citations
- **H-Index Impact**: H-index calculation based on citing papers

## 🔧 Troubleshooting

### No Data Showing

1. Check if GitHub Actions are running successfully.
2. Verify your `SERPAPI_KEY` and Cloudflare secrets (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_KV_NAMESPACE_ID`) are correctly configured in GitHub Secrets.
3. Check the Actions logs for any error messages from Wrangler or the Python script.
4. Test locally: Run `python fetch_citations.py` to see if `citations_data.json` is created correctly.

### API Limits

- SerpAPI free tier: 100 searches/month
- Each run uses 1-2 API calls
- Running daily = ~30-60 calls/month (well within free limits)
- Can increase frequency if needed

### Citations Not Found

- Very new papers may not have citations yet
- Some citations may not be indexed by Google Scholar
- arXiv papers sometimes take time to appear in citation databases

## 📈 Future Enhancements

Potential improvements you could add:

- **Email Notifications**: Alert when new citations are found
- **Multiple Papers**: Track citations for multiple papers
- **Export Features**: Download citation data as CSV/BibTeX
- **Citation Analysis**: Analyze citing paper topics and authors
- **Historical Data**: Long-term citation trend analysis

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the citation tracker!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **SerpAPI** for Google Scholar access
- **Cloudflare** for lightning-fast deployment and hosting
- **Chart.js** for beautiful charts
- **GitHub Actions** for automated updates
- **arXiv** for open access to research papers

---

**Happy Citation Tracking! 📚✨**
