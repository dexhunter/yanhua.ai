#!/usr/bin/env python3
"""
Hybrid Citation Tracker Script
Fetches citations using both a corrected SerpAPI method (for broad coverage) and a
direct search of the HTML versions of recent arXiv papers in cs.AI.
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import requests
import xml.etree.ElementTree as ET
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
    published_date_sort: str = "1900-01-01"
    citations: int = 0
    institutions: str = "Unknown"

    def __hash__(self):
        normalized_title = re.sub(r'\s+', ' ', self.title).strip().lower()
        return hash(normalized_title)

    def __eq__(self, other):
        if not isinstance(other, Paper):
            return NotImplemented
        normalized_title_self = re.sub(r'\s+', ' ', self.title).strip().lower()
        normalized_title_other = re.sub(r'\s+', ' ', other.title).strip().lower()
        return normalized_title_self == normalized_title_other

class CitationTracker:
    """Handles fetching and processing citations from both SerpAPI and arXiv HTML."""

    def __init__(self, serpapi_key: str, target_paper_url: str = "https://www.arxiv.org/abs/2502.13138"):
        self.serpapi_key = serpapi_key
        self.target_paper_url = target_paper_url
        self.serpapi_base_url = "https://serpapi.com/search"
        self.arxiv_api_url = "http://export.arxiv.org/api/query"
        self.target_arxiv_id = self._extract_arxiv_id(target_paper_url)
        self.cache_file = "serpapi_cache.json"
        self.cache_expiry_days = 7
        logger.info(f"Tracking citations for paper: aideml (arXiv ID: {self.target_arxiv_id})")

    def _extract_arxiv_id(self, url: str) -> str:
        match = re.search(r'arxiv\.org/(?:abs|html)/([0-9]+\.[0-9]+)', url)
        return match.group(1) if match else "2502.13138"

    # --- Caching Methods ---
    def _load_cache(self) -> Optional[List[Dict]]:
        """Loads raw paper data from the cache if it exists and is not expired."""
        if not os.path.exists(self.cache_file):
            logger.info("Cache file not found. Fetching from source.")
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            timestamp_str = cache_data.get("timestamp")
            if not timestamp_str:
                logger.warning("Cache is missing timestamp. Ignoring.")
                return None

            timestamp = datetime.fromisoformat(timestamp_str)
            if datetime.now() - timestamp > timedelta(days=self.cache_expiry_days):
                logger.info("Cache is expired. Fetching from source.")
                return None

            logger.info("Loading raw SerpAPI results from cache.")
            return cache_data.get("papers", [])
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error reading cache file: {e}. Ignoring cache.")
            return None

    def _save_cache(self, papers_data: List[Dict]):
        """Saves the raw fetched paper data to the cache file."""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "papers": papers_data
        }
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(papers_data)} raw paper results to SerpAPI cache.")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    # --- SerpAPI Methods (Corrected Two-Step Process) ---
    def _get_serpapi_cites_id(self) -> str:
        """First, find the paper on Google Scholar to get its 'cites_id'."""
        logger.info("SerpAPI: Step 1 - Fetching cites_id for target paper...")
        params = {
            "engine": "google_scholar",
            "q": f"arxiv:{self.target_arxiv_id}",
            "api_key": self.serpapi_key,
        }
        try:
            response = requests.get(self.serpapi_base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            organic_results = data.get('organic_results', [])
            if organic_results:
                cited_by = organic_results[0].get('inline_links', {}).get('cited_by', {})
                cites_id = cited_by.get('cites_id')
                if cites_id:
                    logger.info(f"SerpAPI: Found cites_id: {cites_id}")
                    return cites_id
        except requests.exceptions.RequestException as e:
            logger.error(f"SerpAPI request for cites_id failed: {e}")
        logger.error("SerpAPI: Could not find cites_id for the target paper.")
        return ""

    def _fetch_from_serpapi(self, max_results: int) -> List[Paper]:
        # Try to load from cache first
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        cached_papers_data = self._load_cache()
        if cached_papers_data is not None:
            return [self._parse_serpapi_paper(res) for res in cached_papers_data]

        # If cache is invalid or missing, fetch from SerpAPI
        cites_id = self._get_serpapi_cites_id()
        if not cites_id:
            return []

        logger.info("SerpAPI: Step 2 - Fetching citing papers using cites_id...")
        papers = []
        raw_results = []
        params = {
            "engine": "google_scholar",
            "cites": cites_id,
            "api_key": self.serpapi_key,
            "num": 20, # Google Scholar pages usually have 10 or 20 results
        }
        try:
            response = requests.get(self.serpapi_base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"SerpAPI raw response: {json.dumps(data, indent=2)}")
            raw_results = data.get('organic_results', [])
            if raw_results:
                papers.extend([self._parse_serpapi_paper(res) for res in raw_results])
            
            logger.info(f"SerpAPI: Fetched {len(papers)} papers.")
            # Save the raw results to the cache
            self._save_cache(raw_results)
            return papers
        except requests.exceptions.RequestException as e:
            logger.error(f"SerpAPI request for citing papers failed: {e}")
            return []

    def _parse_serpapi_paper(self, result: Dict) -> Paper:
        title = result.get('title', 'Untitled')
        authors_info = result.get('publication_info', {}).get('summary', '')
        link = result.get('link', '')
        snippet = result.get('snippet', '')
        citations = result.get('inline_links', {}).get('cited_by', {}).get('total', 0)
        
        # --- Improved Date Parsing ---
        publication_info_summary = result.get('publication_info', {}).get('summary', '')
        logger.info(f"Attempting to parse date from: {publication_info_summary}")

        published_date = "Unknown"
        published_date_sort = "1900-01-01"
        
        # Attempt to parse a full date like "Mon, 01 Jan 2024" or "2024"
        try:
            # First, try to find a full date string and parse it
            date_match = re.search(r'\b\w{3}, \d{2} \w{3} \d{4}\b', publication_info_summary) # Simplified, adjust as needed
            if not date_match: # Fallback for formats like "Jan 1, 2024"
                date_match = re.search(r'\b\w{3} \d{1,2}, \d{4}\b', publication_info_summary)
            if not date_match: # Fallback for formats like "YYYY-MM-DD"
                date_match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', publication_info_summary)

            if date_match:
                date_str = date_match.group(0)
                # Try parsing different common formats
                for fmt in ("%b %d, %Y", "%a, %d %b %Y", "%Y-%m-%d"):
                    try:
                        dt_obj = datetime.strptime(date_str, fmt)
                        published_date = dt_obj.strftime('%B %d, %Y')
                        published_date_sort = dt_obj.strftime('%Y-%m-%d')
                        break
                    except ValueError:
                        continue
            else:
                # If no full date, fall back to year extraction from the link
                year_match = re.search(r'arxiv\.org/abs/(\d{2})(\d{2})', link)
                if year_match:
                    year = int("20" + year_match.group(1))
                    month = int(year_match.group(2))
                    published_date = f"{datetime(year, month, 1).strftime('%B')} {year}"
                    published_date_sort = f"{year}-{month:02d}-01"
                else:
                    year_match = re.search(r'\b(19|20)\d{2}\b', publication_info_summary)
                    if year_match:
                        year = int(year_match.group(0))
                        published_date = str(year)
                        published_date_sort = f"{year}-01-01"
        except Exception as e:
            logger.warning(f"Could not parse date from '{publication_info_summary}' or '{link}': {e}")

        return Paper(
            title=title, authors=authors_info, journal="Google Scholar Result",
            snippet=snippet, link=link, published_date=published_date,
            published_date_sort=published_date_sort, citations=citations
        )

    def _find_citations_in_latest_arxiv_via_api(self) -> List[Paper]:
        """
        Uses the arXiv API to directly find papers that cite the target paper.
        This is more reliable and efficient than searching HTML.
        """
        search_query = f'all:"{self.target_arxiv_id}"'
        logger.info(f"arXiv API Search: Finding papers citing {self.target_arxiv_id}")
        
        params = {
            'search_query': search_query,
            'max_results': 100, # Max reasonable number of citations to expect
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(self.arxiv_api_url, params=params, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            atom_namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            for entry in root.findall('atom:entry', atom_namespace):
                paper = self._parse_arxiv_xml_entry(entry, atom_namespace)
                # Ensure the found paper is not the target paper itself
                if paper and self._extract_arxiv_id(paper.link) != self.target_arxiv_id:
                    papers.append(paper)
            
            logger.info(f"arXiv API Search: Found {len(papers)} citing papers.")
            return papers
        except Exception as e:
            logger.error(f"arXiv API search for citing papers failed: {e}")
            return []

    # --- arXiv HTML Search Methods for very recent papers ---
    def _fetch_latest_arxiv_papers_for_scraping(self) -> List[Paper]:
        """Fetches the most recent papers from relevant CS categories to scan their HTML."""
        search_query = "cat:cs.AI OR cat:cs.LG"
        logger.info(f"arXiv HTML Search: Fetching recent papers from categories: {search_query}")
        params = {
            'search_query': search_query,
            'max_results': 100, # Check the latest 100 papers in these specific categories
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        try:
            response = requests.get(self.arxiv_api_url, params=params, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            atom_namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            # Limit scraping to papers submitted in the last 3 days to keep it fast
            three_days_ago = datetime.now() - timedelta(days=3)
            
            for entry in root.findall('atom:entry', atom_namespace):
                paper = self._parse_arxiv_xml_entry(entry, atom_namespace)
                if paper:
                    paper_date = datetime.strptime(paper.published_date_sort, '%Y-%m-%d')
                    if paper_date >= three_days_ago:
                        papers.append(paper)

            logger.info(f"arXiv HTML Search: Found {len(papers)} recent papers from the last 3 days to check.")
            return papers
        except Exception as e:
            logger.error(f"arXiv HTML Search: Could not fetch recent papers for scraping: {e}")
            return []

    def _search_html_for_citation(self, paper: Paper) -> bool:
        """Checks the HTML version of a paper for a citation to the target paper."""
        paper_id = self._extract_arxiv_id(paper.link)
        # Check both v1, v2, etc.
        html_url = f"https://arxiv.org/html/{paper_id}"

        logger.debug(f"Checking HTML: {html_url}")
        try:
            # A short timeout is crucial here to avoid getting stuck.
            response = requests.get(html_url, timeout=15)
            if response.status_code == 200:
                # Simple string search is much faster than regex for this.
                # We check for both the plain ID and the project name "aideml".
                text_to_search = response.text.lower()
                if self.target_arxiv_id in text_to_search or "aide" in text_to_search:
                    logger.info(f"  -> Found citation in {paper.title}")
                    return True
        except requests.exceptions.RequestException:
            # This is expected to happen sometimes (e.g., timeouts, 404s for withdrawn papers)
            pass
        return False

    def _find_citations_in_latest_arxiv_via_html(self) -> List[Paper]:
        """Orchestrates the process of fetching and scraping recent papers."""
        recent_papers = self._fetch_latest_arxiv_papers_for_scraping()
        # We check papers concurrently in a real implementation, but sequentially is fine for this script
        citing_papers = [paper for paper in recent_papers if self._search_html_for_citation(paper)]
        logger.info(f"arXiv HTML Search: Found {len(citing_papers)} new citing papers.")
        return citing_papers

    def _parse_arxiv_xml_entry(self, entry: ET.Element, namespace: Dict) -> Optional[Paper]:
        try:
            paper_id_url = entry.find("atom:id", namespace).text
            title = entry.find('atom:title', namespace).text.strip()
            authors = ", ".join([a.find('atom:name', namespace).text for a in entry.findall('atom:author', namespace)])
            summary = entry.find('atom:summary', namespace).text.strip()
            published_raw = entry.find('atom:published', namespace).text
            published_dt = datetime.fromisoformat(published_raw.replace('Z', '+00:00'))
            published_date = published_dt.strftime('%B %d, %Y')
            published_date_sort = published_dt.strftime('%Y-%m-%d')
            
            return Paper(title=title, authors=authors, journal="arXiv", snippet=summary,
                         link=paper_id_url, published_date=published_date,
                         published_date_sort=published_date_sort)
        except Exception:
            return None

    # --- Data Analysis and Statistics ---
    def _calculate_statistics(self, papers: List[Paper]) -> Dict:
        """Calculates h-index, recent citations, monthly average, and timeline."""
        if not papers:
            return {
                'total_citations': 0, 'h_index': 0, 'recent_citations': 0,
                'avg_citations_per_month': "0.00", 'timeline': []
            }

        # H-Index Calculation
        sorted_by_citations = sorted([p.citations for p in papers if p.citations > 0], reverse=True)
        h_index = 0
        for i, citation_count in enumerate(sorted_by_citations):
            if i + 1 <= citation_count:
                h_index = i + 1
            else:
                break

        # Filter for papers with valid, full dates for all other stats
        valid_papers = []
        for p in papers:
            try:
                # Ensure the sort date is a valid YYYY-MM-DD format
                datetime.strptime(p.published_date_sort, '%Y-%m-%d')
                if not p.published_date_sort.startswith("1900"):
                    valid_papers.append(p)
            except ValueError:
                continue
        
        # Sort valid papers by date for all calculations
        valid_papers.sort(key=lambda p: p.published_date_sort)

        # Recent Citations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_citations = sum(1 for paper in valid_papers if datetime.strptime(paper.published_date_sort, '%Y-%m-%d') >= thirty_days_ago)

        # Average Citations per Month & Timeline
        timeline = []
        avg_citations_per_month = "0.00"
        
        if valid_papers:
            # Timeline
            citations_by_month = {}
            for paper in valid_papers:
                month_key = datetime.strptime(paper.published_date_sort, '%Y-%m-%d').strftime('%Y-%m')
                citations_by_month[month_key] = citations_by_month.get(month_key, 0) + 1

            sorted_months = sorted(citations_by_month.keys())

            cumulative_citations = 0
            for month in sorted_months:
                cumulative_citations += citations_by_month[month]
                timeline.append({'date': f"{month}-01", 'citations': cumulative_citations})


            # Monthly Average
            first_month = datetime.strptime(valid_papers[0].published_date_sort, '%Y-%m-%d')
            last_month = datetime.strptime(valid_papers[-1].published_date_sort, '%Y-%m-%d')
            total_months = (last_month.year - first_month.year) * 12 + last_month.month - first_month.month + 1
            avg_citations_per_month = f"{(len(valid_papers) / total_months):.2f}" if total_months > 0 else "0.00"

        return {
            'total_citations': len(papers),
            'h_index': h_index,
            'recent_citations': recent_citations,
            'avg_citations_per_month': avg_citations_per_month,
            'timeline': timeline
        }

    # --- Main Orchestration ---
    def fetch_citations(self, max_results: int = 200) -> List[Paper]:
        logger.info("Starting hybrid citation search...")
        
        # 1. Get broad results from Google Scholar
        serpapi_papers = self._fetch_from_serpapi(max_results)
        
        # 2. Get reliable, indexed citations directly from the arXiv API
        arxiv_api_papers = self._find_citations_in_latest_arxiv_via_api()
        
        # 3. Scrape the very latest papers for unindexed citations
        arxiv_html_papers = self._find_citations_in_latest_arxiv_via_html()

        # Merge all sources and remove duplicates
        merged_papers = list(set(serpapi_papers + arxiv_api_papers + arxiv_html_papers))
        
        # Sort by the reliable date field, newest first
        merged_papers.sort(key=lambda p: p.published_date_sort, reverse=True)
        
        logger.info(f"Fetched a total of {len(merged_papers)} unique citing papers from all sources.")
        return merged_papers

    def save_data(self, papers: List[Paper], filename: str = 'citations_data.json'):
        stats = self._calculate_statistics(papers)
        data = {
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'target_paper': self.target_paper_url,
            'arxiv_id': self.target_arxiv_id,
            **stats,
            'papers': [
                {
                    'title': paper.title, 'authors': paper.authors, 'journal': paper.journal,
                    'snippet': paper.snippet, 'link': paper.link, 'published_date': paper.published_date,
                    'published_date_sort': paper.published_date_sort, 'citations': paper.citations,
                    'institutions': paper.institutions
                }
                for paper in papers
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filename}")

def main():
    load_dotenv()
    serpapi_key = os.getenv('SERPAPI_KEY')
    if not serpapi_key:
        logger.error("SERPAPI_KEY not found. Please set it in your .env file or environment variables.")
        return

    tracker = CitationTracker(serpapi_key=serpapi_key)
    
    try:
        papers = tracker.fetch_citations(max_results=100)
        # Write to the correct path for the Pages Function
        tracker.save_data(papers, filename='functions/citations_data.json')
        logger.info("Citation tracking completed successfully!")
    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()