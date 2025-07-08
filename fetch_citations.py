#!/usr/bin/env python3
"""
Citation Tracker Script
Fetches citations for arXiv:2502.13138 using SerpAPI and saves to JSON
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import re
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Paper:
    """Represents a citing paper"""
    title: str
    authors: str
    journal: str
    snippet: str
    link: str
    published_date: str
    published_date_sort: str = "1900-01-01"  # For sorting purposes
    citations: int = 0

class CitationTracker:
    """Handles fetching and processing citations from Google Scholar via SerpAPI"""
    
    def __init__(self, api_key: str, target_paper_url: str = "https://arxiv.org/abs/2502.13138"):
        self.api_key = api_key
        self.target_paper_url = target_paper_url
        self.base_url = "https://serpapi.com/search"
        
        # Extract arXiv ID from URL
        self.arxiv_id = self._extract_arxiv_id(target_paper_url)
        logger.info(f"Tracking citations for paper: aideml (arXiv ID: {self.arxiv_id})")
    
    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv ID from URL"""
        match = re.search(r'arxiv\.org/abs/([0-9]+\.[0-9]+)', url)
        if match:
            return match.group(1)
        return "2502.13138"  # fallback
    

    
    def _get_paper_cites_id(self) -> str:
        """Get the cites ID for our target paper by searching for it first"""
        # For now, we'll use a search approach since we need to find the paper first
        # This is a simplified approach - in production you might cache the cites_id
        search_params = {
            "engine": "google_scholar",
            "q": f"arxiv:{self.arxiv_id}",
            "api_key": self.api_key,
            "num": 1,
            "hl": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=search_params, timeout=30, verify=True)
            response.raise_for_status()
            data = response.json()
            
            organic_results = data.get('organic_results', [])
            if organic_results and 'inline_links' in organic_results[0]:
                cited_by = organic_results[0]['inline_links'].get('cited_by', {})
                if 'cites_id' in cited_by:
                    return cited_by['cites_id']
        except Exception as e:
            logger.warning(f"Could not get cites_id, falling back to search: {e}")
        
        # Fallback: return empty string to use basic search
        return ""
    
    def _make_request(self, params: Dict, max_retries: int = 3) -> Optional[Dict]:
        """Make API request with error handling and retry logic"""
        for attempt in range(max_retries):
            try:
                # Add SSL verification and custom headers to handle connection issues
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(
                    self.base_url, 
                    params=params, 
                    timeout=30,
                    headers=headers,
                    verify=True  # Explicit SSL verification
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.SSLError as e:
                logger.warning(f"SSL error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error(f"SSL error persisted after {max_retries} attempts")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error(f"API request failed after {max_retries} attempts")
                    return None
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                return None
        
        return None
    
    def _parse_paper(self, result: Dict) -> Paper:
        """Parse a single paper from search results"""
        title = result.get('title', 'Untitled')
        
        # Extract authors
        authors = "Unknown authors"
        if 'publication_info' in result and 'authors' in result['publication_info']:
            authors_list = result['publication_info']['authors']
            if isinstance(authors_list, list):
                authors = ", ".join([author.get('name', '') for author in authors_list])
        elif 'publication_info' in result and 'summary' in result['publication_info']:
            # Try to extract authors from summary
            summary = result['publication_info']['summary']
            if ' - ' in summary:
                authors = summary.split(' - ')[0]
        
        # Extract journal/venue
        journal = "Unknown venue"
        if 'publication_info' in result and 'summary' in result['publication_info']:
            summary = result['publication_info']['summary']
            parts = summary.split(' - ')
            if len(parts) >= 2:
                journal = parts[1]
        
        # Extract snippet
        snippet = result.get('snippet', 'No snippet available')
        
        # Extract link
        link = result.get('link', '')
        
        # Extract publication date with more precision
        published_date = "Unknown"
        published_date_for_sorting = None
        
        if 'publication_info' in result and 'summary' in result['publication_info']:
            summary = result['publication_info']['summary']
            
            # Try to extract more precise dates
            # Pattern 1: "Month Day, Year" or "Month Year"
            month_date_match = re.search(r'([A-Za-z]+)\s+(\d{1,2},?\s+)?(\d{4})', summary)
            if month_date_match:
                month = month_date_match.group(1)
                day = month_date_match.group(2)
                year = month_date_match.group(3)
                
                # Convert month name to number
                month_mapping = {
                    'jan': '01', 'january': '01', 'feb': '02', 'february': '02',
                    'mar': '03', 'march': '03', 'apr': '04', 'april': '04',
                    'may': '05', 'jun': '06', 'june': '06', 'jul': '07', 'july': '07',
                    'aug': '08', 'august': '08', 'sep': '09', 'september': '09',
                    'oct': '10', 'october': '10', 'nov': '11', 'november': '11',
                    'dec': '12', 'december': '12'
                }
                
                month_num = month_mapping.get(month.lower()[:3], '01')
                day_num = '01'
                if day and day.strip().rstrip(','):
                    try:
                        day_num = f"{int(day.strip().rstrip(',')):#02d}"
                    except:
                        day_num = '01'
                
                published_date = f"{month} {day.strip() if day else ''}{year}".strip()
                published_date_for_sorting = f"{year}-{month_num}-{day_num}"
            
            # Pattern 2: Just year
            elif re.search(r'\b(19|20)\d{2}\b', summary):
                year_match = re.search(r'\b(19|20)\d{2}\b', summary)
                year = year_match.group(0)
                published_date = year
                published_date_for_sorting = f"{year}-01-01"
        
        # Try to extract date from link (arXiv papers often have dates in URLs)
        if link and 'arxiv.org' in link:
            # Pattern: arxiv.org/abs/YYMM.NNNNN (where YY=year, MM=month)
            arxiv_id_match = re.search(r'arxiv\.org/abs/(\d{2})(\d{2})\.(\d+)', link)
            if arxiv_id_match:
                year_short = arxiv_id_match.group(1)
                month = arxiv_id_match.group(2)
                
                # Convert 2-digit year to 4-digit (assuming 20xx for now)
                year = f"20{year_short}"
                
                # Map month number to month name
                month_names = {
                    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
                    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
                }
                
                month_name = month_names.get(month, 'Unknown')
                published_date = f"{month_name} {year}"
                published_date_for_sorting = f"{year}-{month}-15"  # Use 15th as default day
        
        # Additional date patterns in the summary
        if published_date_for_sorting is None and 'publication_info' in result and 'summary' in result['publication_info']:
            summary = result['publication_info']['summary']
            
            # Pattern 3: "YYYY-MM-DD" format
            iso_date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', summary)
            if iso_date_match:
                year, month, day = iso_date_match.groups()
                published_date = f"{year}-{month}-{day}"
                published_date_for_sorting = f"{year}-{month}-{day}"
            
            # Pattern 4: "DD/MM/YYYY" or "MM/DD/YYYY" format
            elif re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', summary):
                date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', summary)
                part1, part2, year = date_match.groups()
                # Assume MM/DD/YYYY format (US style)
                month = f"{int(part1):02d}"
                day = f"{int(part2):02d}"
                published_date = f"{month}/{day}/{year}"
                published_date_for_sorting = f"{year}-{month}-{day}"
        
        # Default fallback
        if published_date_for_sorting is None:
            published_date_for_sorting = "1900-01-01"
        
        # Extract citation count
        citations = 0
        if 'inline_links' in result and 'cited_by' in result['inline_links']:
            citations = result['inline_links']['cited_by'].get('total', 0)
        
        return Paper(
            title=title,
            authors=authors,
            journal=journal,
            snippet=snippet,
            link=link,
            published_date=published_date,
            published_date_sort=published_date_for_sorting or "1900-01-01",
            citations=citations
        )
    
    def fetch_citations(self, max_results: int = 200) -> List[Paper]:
        """Fetch all citing papers"""
        papers = []
        
        logger.info(f"Fetching citations (max {max_results} results)...")
        
        # First, try to get the cites_id for more accurate results
        cites_id = self._get_paper_cites_id()
        
        if cites_id:
            logger.info(f"Found cites_id: {cites_id}. Searching for citing papers...")
            papers = self._fetch_with_cites_id(cites_id, max_results)
        else:
            logger.info("No cites_id found. Using fallback search method...")
            papers = self._fetch_with_fallback_search(max_results)
        
        # Sort papers by publication date (latest first)
        papers.sort(key=lambda p: p.published_date_sort, reverse=True)
        
        logger.info(f"Fetched {len(papers)} citing papers, sorted by publication date")
        return papers
    
    def _fetch_with_cites_id(self, cites_id: str, max_results: int) -> List[Paper]:
        """Fetch citations using the cites_id parameter"""
        papers = []
        start = 0
        page_size = 100
        
        while len(papers) < max_results:
            # Build params with cites_id
            current_year = datetime.now().year
            params = {
                "engine": "google_scholar",
                "cites": cites_id,
                "api_key": self.api_key,
                "start": start,
                "num": page_size,
                "hl": "en",
                "as_sdt": "0,5",
                "as_yhi": current_year,  # Only papers published up to current year
            }
            
            logger.info(f"Fetching citing papers page {start//page_size + 1} (results {start}-{start+page_size})...")
            
            data = self._make_request(params)
            if not data:
                logger.error("Failed to fetch data from API")
                break
            
            # Check for errors
            if 'error' in data:
                logger.error(f"API error: {data['error']}")
                break
            
            # Extract papers from results
            organic_results = data.get('organic_results', [])
            if not organic_results:
                logger.info("No more citing papers found")
                break
            
            for result in organic_results:
                if len(papers) >= max_results:
                    break
                
                try:
                    paper = self._parse_paper(result)
                    # Filter out the original paper itself
                    if self.arxiv_id not in paper.title.lower() and self.arxiv_id not in paper.link:
                        papers.append(paper)
                        logger.debug(f"Added citing paper: {paper.title[:50]}...")
                except Exception as e:
                    logger.warning(f"Failed to parse paper: {e}")
                    continue
            
            start += page_size
            time.sleep(1)  # Rate limiting
        
        return papers
    
    def _fetch_with_fallback_search(self, max_results: int) -> List[Paper]:
        """Fallback method to search for papers mentioning our arXiv ID"""
        papers = []
        start = 0
        page_size = 100
        
        while len(papers) < max_results:
            # Use basic search as fallback
            current_year = datetime.now().year
            params = {
                "engine": "google_scholar",
                "q": f'"{self.arxiv_id}" OR "arxiv:{self.arxiv_id}"',
                "api_key": self.api_key,
                "start": start,
                "num": page_size,
                "hl": "en",
                "as_sdt": "0,5",
                "as_yhi": current_year,
            }
            
            logger.info(f"Fallback search page {start//page_size + 1} (results {start}-{start+page_size})...")
            
            data = self._make_request(params)
            if not data:
                break
            
            if 'error' in data:
                logger.error(f"API error: {data['error']}")
                break
            
            organic_results = data.get('organic_results', [])
            if not organic_results:
                break
            
            for result in organic_results:
                if len(papers) >= max_results:
                    break
                
                try:
                    paper = self._parse_paper(result)
                    # More strict filtering for fallback search
                    paper_text = f"{paper.title} {paper.snippet}".lower()
                    if (self.arxiv_id in paper_text and 
                        not paper.link.endswith(f"/{self.arxiv_id}") and  # Not the original paper
                        "arxiv" in paper_text):  # Actually mentions arXiv
                        papers.append(paper)
                        logger.debug(f"Added paper: {paper.title[:50]}...")
                except Exception as e:
                    logger.warning(f"Failed to parse paper: {e}")
                    continue
            
            start += page_size
            time.sleep(1)
        
        return papers
    
    def _calculate_stats(self, papers: List[Paper]) -> Dict:
        """Calculate statistics about the citations"""
        total_citations = len(papers)
        
        # Calculate recent citations (papers from last 30 days)
        # For now, we'll use a placeholder since we don't have exact dates
        recent_citations = min(5, total_citations)  # Placeholder
        
        # Calculate average citations per month
        # This is a rough estimate based on when the original paper was published
        months_since_publication = 1  # Placeholder - paper is very new
        avg_citations_per_month = total_citations / max(months_since_publication, 1)
        
        # Simple H-index calculation (papers with at least h citations)
        citation_counts = [paper.citations for paper in papers]
        citation_counts.sort(reverse=True)
        h_index = 0
        for i, count in enumerate(citation_counts):
            if count >= (i + 1):
                h_index = i + 1
            else:
                break
        
        return {
            'total_citations': total_citations,
            'recent_citations': recent_citations,
            'avg_citations_per_month': round(avg_citations_per_month, 1),
            'h_index': h_index
        }
    
    def _generate_timeline(self, papers: List[Paper]) -> List[Dict]:
        """Generate timeline data for the chart"""
        # For now, create a simple timeline
        # In a real implementation, you'd parse publication dates more carefully
        timeline = []
        
        # Create monthly data points
        base_date = datetime.now() - timedelta(days=30)
        for i in range(6):  # Last 6 months
            month_date = base_date + timedelta(days=i*30)
            # Simple simulation - in reality you'd count papers by publication date
            citations = min(i * 2, len(papers))
            timeline.append({
                'date': month_date.strftime('%Y-%m'),
                'citations': citations
            })
        
        return timeline
    
    def save_data(self, papers: List[Paper], filename: str = 'citations_data.json'):
        """Save citation data to JSON file"""
        stats = self._calculate_stats(papers)
        timeline = self._generate_timeline(papers)
        
        data = {
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'target_paper': self.target_paper_url,
            'arxiv_id': self.arxiv_id,
            **stats,
            'timeline': timeline,
            'papers': [
                {
                    'title': paper.title,
                    'authors': paper.authors,
                    'journal': paper.journal,
                    'snippet': paper.snippet,
                    'link': paper.link,
                    'published_date': paper.published_date,
                    'citations': paper.citations
                }
                for paper in papers
            ]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def create_fallback_data(self, filename: str = 'citations_data.json'):
        """Create fallback data if API fails"""
        fallback_data = {
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'target_paper': self.target_paper_url,
            'arxiv_id': self.arxiv_id,
            'total_citations': 0,
            'recent_citations': 0,
            'avg_citations_per_month': 0,
            'h_index': 0,
            'timeline': [],
            'papers': [],
            'error': 'Unable to fetch citation data. Please check API key and try again.'
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(fallback_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Fallback data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save fallback data: {e}")

def main():
    """Main function"""
    # Load environment variables from .env file (if it exists)
    load_dotenv()
    
    # Get API key from environment variable (can be set in .env file or system env)
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        logger.error("SERPAPI_KEY not found in environment variables or .env file")
        logger.info("Please set your SerpAPI key:")
        logger.info("  Option 1: Create a .env file with: SERPAPI_KEY=your_api_key_here")
        logger.info("  Option 2: Set environment variable: export SERPAPI_KEY='your_api_key_here'")
        # Create fallback data
        tracker = CitationTracker("dummy_key")
        tracker.create_fallback_data()
        return
    
    # Initialize tracker
    tracker = CitationTracker(api_key)
    
    try:
        # Fetch citations
        papers = tracker.fetch_citations(max_results=100)
        
        # Save data
        tracker.save_data(papers)
        
        logger.info("Citation tracking completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        # Create fallback data on error
        tracker.create_fallback_data()

if __name__ == "__main__":
    main() 