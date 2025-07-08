# 📚 aideml - Citation Tracker

An automated citation tracking website that monitors and displays papers citing our research. The site automatically updates by committing new data directly to the repository via a GitHub Action.

## 🌟 Features

- **Automated Citation Tracking**: Uses SerpAPI and direct arXiv searches to find citing papers.
- **Beautiful Web Interface**: Modern, responsive design with interactive charts.
- **Real-time Statistics**: Total citations, recent citations, H-index, and trends.
- **GitHub Actions Integration**: Automatically updates daily by pushing a new data file.
- **Cloudflare Pages Deployment**: Fast, simple, and free deployment.
- **Mobile Responsive**: Works perfectly on all devices.

## 🚀 Live Demo

The website is automatically deployed on **Cloudflare Pages**. The citation data is updated daily by a GitHub Action that commits the new data directly to this repository, which in turn triggers a new deployment.

## 📋 Setup Instructions

### 1. Fork/Clone this Repository

```bash
git clone https://github.com/yourusername/yanhua.ai.git
cd yanhua.ai
```

### 2. Get a SerpAPI Key

1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for a free account (100 searches/month is plenty).
3. Get your API key from the dashboard.

### 3. Configure GitHub Secrets

For the automation to work, you need to give the GitHub Action a SerpAPI key and the permission to push changes back to your repository.

1. Go to your forked repository's **Settings** tab.
2. Navigate to **Secrets and variables** → **Actions**.
3. Add the following new secret:
   - `SERPAPI_KEY`: Your API key from SerpAPI.

4.  Next, you need to allow the Action to write back to your repository.
    *   Still in **Settings**, go to **Actions** -> **General**.
    *   Scroll down to the **Workflow permissions** section.
    *   Select the **Read and write permissions** option.
    *   Click **Save**.

### 4. Deploy on Cloudflare Pages

1.  Go to your Cloudflare dashboard.
2.  Navigate to **Workers & Pages** and click **Create application**.
3.  Select the **Pages** tab and click **Connect to Git**.
4.  Connect your GitHub account and select your forked repository.
5.  In the **Build settings**, select the **Node.js** preset.
6.  Set the **Build command** to `npm install`.
7.  Leave the **Build output directory** as is (it's not used for this project).
8.  Click **Save and Deploy**.

That's it! Your site will be live, and the GitHub Action will keep the data up-to-date automatically.

### 5. Customize for Your Paper (Optional)

If you want to track a different arXiv paper:

1. Edit `fetch_citations.py`.
2. Change the `target_paper_url` in the `CitationTracker` initialization.
3. Update the paper reference in `index.html`.

## 🔄 How It Works

The system is simple and robust:

1.  **Daily Schedule**: A GitHub Action runs automatically once a day.
2.  **Fetch Citations**: The `fetch_citations.py` script runs, searching SerpAPI and arXiv for new citing papers.
3.  **Generate Data File**: The script generates an updated `functions/citations_data.json` file.
4.  **Commit to Repository**: The Action commits this new data file directly to the `main` branch.
5.  **Trigger Deployment**: This new commit automatically triggers a new build and deployment on Cloudflare Pages, making the new data live.

## 📁 Project Structure

```
├── index.html                      # Main website file
├── functions/
│   ├── api/[[path]].js             # Cloudflare Pages Function to serve the data
│   └── citations_data.json         # The citation data (auto-generated)
├── fetch_citations.py              # Citation tracking script
├── requirements.txt                # Python dependencies
├── package.json                    # Node.js dependencies
├── .github/workflows/
│   └── update-citations.yml        # GitHub Actions workflow
└── README.md                       # This file
```

## 🛠 Technical Details

- **Python 3.9+**
- **requests**: For API calls
- **Hono**: For the Cloudflare Pages Function
- **GitHub Actions**: For automation
- **Chart.js**: For data visualization

The data is stored in `functions/citations_data.json` and served by a simple Cloudflare Pages Function.

## 🔧 Troubleshooting

### No Data Showing on the Website

1.  Check if the GitHub Action ran successfully after you set up the project. You may need to trigger it manually the first time.
2.  Verify your `SERPAPI_KEY` is correctly configured in GitHub Secrets.
3.  Check the Actions logs for any error messages from the Python script.
4.  Test locally: Run `python fetch_citations.py` to see if `functions/citations_data.json` is created correctly.

### Action Fails with a Permissions Error

If the GitHub Action fails with a `403` error, make sure you have set the **Workflow permissions** to **Read and write permissions** in your repository's settings (under Actions -> General).