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
        logger.info(f"Tracking citations for paper: aideml (arXiv ID: {self.target_arxiv_id})")

    def _extract_arxiv_id(self, url: str) -> str:
        match = re.search(r'arxiv\.org/(?:abs|html)/([0-9]+\.[0-9]+)', url)
        return match.group(1) if match else "2502.13138"

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
        cites_id = self._get_serpapi_cites_id()
        if not cites_id:
            return []

        logger.info("SerpAPI: Step 2 - Fetching citing papers using cites_id...")
        papers = []
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
            organic_results = data.get('organic_results', [])
            if organic_results:
                papers.extend([self._parse_serpapi_paper(res) for res in organic_results])
            logger.info(f"SerpAPI: Fetched {len(papers)} papers.")
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
        
        # Extract year from summary, default to unknown
        year_match = re.search(r'\b(19|20)\d{2}\b', authors_info)
        year = year_match.group(0) if year_match else "Unknown"

        return Paper(
            title=title, authors=authors_info, journal="Google Scholar Result",
            snippet=snippet, link=link, published_date=year,
            published_date_sort=f"{year}-01-01", citations=citations
        )

    # --- arXiv HTML Search Methods (Refined to cs.AI) ---
    def _fetch_latest_arxiv_papers(self) -> List[Paper]:
        logger.info("arXiv HTML Search: Fetching recent papers from cs.AI...")
        search_query = "cat:cs.AI"
        params = {
            'search_query': search_query,
            'max_results': 200,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        try:
            response = requests.get(self.arxiv_api_url, params=params, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            atom_namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            one_week_ago = datetime.now() - timedelta(days=7)
            
            for entry in root.findall('atom:entry', atom_namespace):
                paper = self._parse_arxiv_xml_entry(entry, atom_namespace)
                if paper:
                    paper_date = datetime.strptime(paper.published_date_sort, '%Y-%m-%d')
                    if paper_date >= one_week_ago:
                        papers.append(paper)

            logger.info(f"arXiv HTML Search: Found {len(papers)} recent papers from the last 7 days in cs.AI to check.")
            return papers
        except Exception as e:
            logger.error(f"arXiv HTML Search: Could not fetch recent papers: {e}")
        return []

    def _search_html_for_citation(self, paper: Paper) -> bool:
        paper_id = self._extract_arxiv_id(paper.link)
        html_url = f"https://arxiv.org/html/{paper_id}"
        
        logger.debug(f"Checking HTML: {html_url}")
        try:
            response = requests.get(html_url, timeout=20)
            if response.status_code == 200 and self.target_arxiv_id in response.text:
                logger.info(f"  -> Found citation in {paper.title}")
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def _find_citations_in_latest_arxiv(self) -> List[Paper]:
        recent_papers = self._fetch_latest_arxiv_papers()
        citing_papers = [paper for paper in recent_papers if self._search_html_for_citation(paper)]
        return citing_papers

    def _parse_arxiv_xml_entry(self, entry: ET.Element, namespace: Dict) -> Optional[Paper]:
        try:
            paper_id_url = entry.find("atom:id", namespace).text
            title = entry.find('atom:title', namespace).text.strip()
            authors = ", ".join([a.find('atom:name', namespace).text for a in entry.findall('atom:author', namespace)])
            summary = entry.find('atom:summary', namespace).text.strip()
            published_raw = entry.find('atom:published', namespace).text
            published_dt = datetime.fromisoformat(published_raw.replace('Z', '+00:00'))
            published_date = published_dt.strftime('%Y-%m-%d')
            
            return Paper(title=title, authors=authors, journal="arXiv", snippet=summary,
                         link=paper_id_url, published_date=published_date,
                         published_date_sort=published_date)
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

        # Recent Citations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_citations = 0
        for paper in papers:
            try:
                # Handles both 'YYYY-MM-DD' and just 'YYYY'
                date_str = paper.published_date.split(' ')[0]
                paper_date = datetime.strptime(date_str, '%Y-%m-%d')
                if paper_date >= thirty_days_ago:
                    recent_citations += 1
            except (ValueError, IndexError):
                continue

        # Average Citations per Month & Timeline
        timeline = []
        monthly_counts = {}
        
        # Filter for papers with valid, full dates
        valid_papers = []
        for p in papers:
            try:
                datetime.strptime(p.published_date_sort, '%Y-%m-%d')
                valid_papers.append(p)
            except ValueError:
                continue
        
        if valid_papers:
            # Sort papers by date for timeline and monthly calculation
            valid_papers.sort(key=lambda p: p.published_date_sort)
            
            # Timeline
            cumulative_citations = 0
            for paper in valid_papers:
                cumulative_citations += 1
                timeline.append({'date': paper.published_date_sort, 'citations': cumulative_citations})

            # Monthly Average
            first_month = datetime.strptime(valid_papers[0].published_date_sort, '%Y-%m-%d')
            last_month = datetime.strptime(valid_papers[-1].published_date_sort, '%Y-%m-%d')
            total_months = (last_month.year - first_month.year) * 12 + last_month.month - first_month.month + 1
            avg_citations_per_month = f"{(len(valid_papers) / total_months):.2f}" if total_months > 0 else "0.00"
        else:
            avg_citations_per_month = "0.00"


        return {
            'total_citations': len(papers),
            'h_index': h_index,
            'recent_citations': recent_citations,
            'avg_citations_per_month': avg_citations_per_month,
            'timeline': timeline
        }

    # --- Main Orchestration ---
    def fetch_citations(self, max_results: int = 200) -> List[Paper]:
        logger.info("Starting citation search with corrected logic...")
        serpapi_papers = self._fetch_from_serpapi(max_results)
        latest_citing_papers = self._find_citations_in_latest_arxiv()

        merged_papers = list(set(serpapi_papers + latest_citing_papers))
        merged_papers.sort(key=lambda p: p.published_date_sort, reverse=True)
        
        logger.info(f"Fetched a total of {len(merged_papers)} unique citing papers.")
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
                    'citations': paper.citations, 'institutions': paper.institutions
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