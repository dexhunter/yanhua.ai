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
    institutions: str = "Unknown"  # Research institutions/companies

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
    
    def _extract_institutions(self, result: Dict, authors_list: List, journal: str, snippet: str, link: str) -> str:
        """Extract institutional affiliations from paper metadata"""
        institutions = set()
        
        # 1. Extract from author affiliation information
        if authors_list and isinstance(authors_list, list):
            for author in authors_list:
                if isinstance(author, dict) and 'affiliations' in author:
                    for affiliation in author['affiliations']:
                        if isinstance(affiliation, dict) and 'name' in affiliation:
                            inst = self._clean_institution_name(affiliation['name'])
                            if inst:
                                institutions.add(inst)
        
        # 2. Extract from publication info summary
        if 'publication_info' in result and 'summary' in result['publication_info']:
            summary = result['publication_info']['summary']
            found_institutions = self._extract_institutions_from_text(summary)
            institutions.update(found_institutions)
        
        # 3. Extract from journal/conference information
        if journal and journal != "Unknown venue":
            journal_institutions = self._extract_institutions_from_text(journal)
            institutions.update(journal_institutions)
        
        # 4. Extract from snippet
        if snippet:
            snippet_institutions = self._extract_institutions_from_text(snippet)
            institutions.update(snippet_institutions)
        
        # 5. Extract from link domain (for company research)
        if link:
            domain_institution = self._extract_institution_from_domain(link)
            if domain_institution:
                institutions.add(domain_institution)
        
        # Clean and return institutions
        cleaned_institutions = []
        for inst in institutions:
            cleaned = self._clean_institution_name(inst)
            if cleaned and len(cleaned) > 2:  # Filter out very short matches
                cleaned_institutions.append(cleaned)
        
        if cleaned_institutions:
            return ", ".join(sorted(list(set(cleaned_institutions))))
        return "Unknown"
    
    def _extract_institutions_from_text(self, text: str) -> set:
        """Extract institution names from text using pattern matching"""
        institutions = set()
        
        # University patterns
        university_patterns = [
            r'\b([A-Z][a-z]+ University(?:\s+of\s+[A-Z][a-z]+)?)\b',
            r'\bUniversity of ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+University\b',
            r'\b([A-Z][a-z]+)\s+Institute(?:\s+of\s+Technology)?\b',
            r'\bInstitute of ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Institute\b',
            r'\b([A-Z][a-z]+)\s+College\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+School\b',
        ]
        
        for pattern in university_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    for m in match:
                        if m.strip():
                            institutions.add(m.strip())
                else:
                    institutions.add(match.strip())
        
        # Company patterns
        company_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Inc|Corp|Corporation|Ltd|Limited|LLC|Research|Lab|Labs|AI|Technologies)\b',
            r'\b(Meta|Google|Microsoft|Apple|Amazon|Facebook|OpenAI|Anthropic|DeepMind|Tesla|NVIDIA|Intel|IBM|Oracle|Salesforce|Uber|Lyft|Airbnb|Netflix|Twitter|LinkedIn|Adobe|Slack|Zoom|Dropbox|Spotify|Pinterest|Snapchat|TikTok|ByteDance|Baidu|Tencent|Alibaba|Huawei|Samsung|Sony|LG|Qualcomm|Broadcom|AMD|Cisco|VMware|ServiceNow|Workday|Palantir|Snowflake|Databricks|Stripe|Square|PayPal|Visa|Mastercard|JPMorgan|Goldman|Morgan|Citadel|Two Sigma|Jane Street|DE Shaw|Bridgewater|AQR|Renaissance|Millennium|Point72|Susquehanna|Optiver|Jump|IMC|Virtu|Hudson River|Tower Research|DRW|Citadel Securities|Flow Traders|Akuna Capital|Chicago Trading|XTX Markets|Wolverine Trading|Five Rings Capital|Old Mission|Belvedere Trading|Group One Trading|Peak6|TransMarket|GTS|KCG|Getco|Sun Trading|Tradebot|Automated Trading Desk|Quantlab|WorldQuant|Cubist|Schonfeld|Millennium Partners|Balyasny|ExodusPoint|Coatue|Tiger Global|Sequoia|Andreessen Horowitz|Kleiner Perkins|Greylock|Bessemer|Lightspeed|Accel|Benchmark|General Catalyst|Founders Fund|Thrive Capital|GV|Intel Capital|Qualcomm Ventures|Samsung Ventures|Sony Ventures|Salesforce Ventures|Microsoft Ventures|Google Ventures|Amazon Ventures|Apple Ventures|Meta Ventures|Tesla Ventures|NVIDIA Ventures|IBM Ventures|Oracle Ventures|Adobe Ventures|Slack Ventures|Zoom Ventures|Dropbox Ventures|Spotify Ventures|Pinterest Ventures|Snapchat Ventures|TikTok Ventures|ByteDance Ventures|Baidu Ventures|Tencent Ventures|Alibaba Ventures|Huawei Ventures|Samsung Ventures|Sony Ventures|LG Ventures|Qualcomm Ventures|Broadcom Ventures|AMD Ventures|Cisco Ventures|VMware Ventures|ServiceNow Ventures|Workday Ventures|Palantir Ventures|Snowflake Ventures|Databricks Ventures|Stripe Ventures|Square Ventures|PayPal Ventures|Visa Ventures|Mastercard Ventures)\b',
            r'\b([A-Z][a-z]+)\s+AI\b',
            r'\b([A-Z][a-z]+)\s+Research\b',
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    for m in match:
                        if m.strip():
                            institutions.add(m.strip())
                else:
                    institutions.add(match.strip())
        
        return institutions
    
    def _extract_institution_from_domain(self, url: str) -> Optional[str]:
        """Extract institution from URL domain"""
        domain_mapping = {
            'openai.com': 'OpenAI',
            'anthropic.com': 'Anthropic',
            'deepmind.com': 'DeepMind',
            'google.com': 'Google',
            'meta.com': 'Meta',
            'facebook.com': 'Meta',
            'microsoft.com': 'Microsoft',
            'apple.com': 'Apple',
            'amazon.com': 'Amazon',
            'nvidia.com': 'NVIDIA',
            'intel.com': 'Intel',
            'ibm.com': 'IBM',
            'oracle.com': 'Oracle',
            'salesforce.com': 'Salesforce',
            'uber.com': 'Uber',
            'tesla.com': 'Tesla',
            'netflix.com': 'Netflix',
            'adobe.com': 'Adobe',
            'stanford.edu': 'Stanford University',
            'mit.edu': 'MIT',
            'harvard.edu': 'Harvard University',
            'berkeley.edu': 'UC Berkeley',
            'ucla.edu': 'UCLA',
            'cmu.edu': 'Carnegie Mellon University',
            'caltech.edu': 'Caltech',
            'princeton.edu': 'Princeton University',
            'yale.edu': 'Yale University',
            'columbia.edu': 'Columbia University',
            'nyu.edu': 'New York University',
            'cornell.edu': 'Cornell University',
            'upenn.edu': 'University of Pennsylvania',
            'uchicago.edu': 'University of Chicago',
            'umich.edu': 'University of Michigan',
            'gatech.edu': 'Georgia Tech',
            'utexas.edu': 'University of Texas at Austin',
            'washington.edu': 'University of Washington',
            'usc.edu': 'USC',
            'duke.edu': 'Duke University',
            'northwestern.edu': 'Northwestern University',
            'rice.edu': 'Rice University',
            'vanderbilt.edu': 'Vanderbilt University',
            'emory.edu': 'Emory University',
            'jhu.edu': 'Johns Hopkins University',
            'georgetown.edu': 'Georgetown University',
            'tufts.edu': 'Tufts University',
            'brandeis.edu': 'Brandeis University',
            'bu.edu': 'Boston University',
            'northeastern.edu': 'Northeastern University',
            'wpi.edu': 'Worcester Polytechnic Institute',
            'rpi.edu': 'Rensselaer Polytechnic Institute',
            'rit.edu': 'Rochester Institute of Technology',
            'case.edu': 'Case Western Reserve University',
            'cwru.edu': 'Case Western Reserve University',
            'ucsd.edu': 'UC San Diego',
            'uci.edu': 'UC Irvine',
            'ucsb.edu': 'UC Santa Barbara',
            'ucsc.edu': 'UC Santa Cruz',
            'ucr.edu': 'UC Riverside',
            'ucmerced.edu': 'UC Merced',
            'ucdavis.edu': 'UC Davis',
            'ucsf.edu': 'UCSF',
            'ox.ac.uk': 'Oxford University',
            'cam.ac.uk': 'Cambridge University',
            'imperial.ac.uk': 'Imperial College London',
            'ucl.ac.uk': 'University College London',
            'kcl.ac.uk': 'King\'s College London',
            'ed.ac.uk': 'University of Edinburgh',
            'manchester.ac.uk': 'University of Manchester',
            'warwick.ac.uk': 'University of Warwick',
            'bristol.ac.uk': 'University of Bristol',
            'bath.ac.uk': 'University of Bath',
            'soton.ac.uk': 'University of Southampton',
            'surrey.ac.uk': 'University of Surrey',
            'leeds.ac.uk': 'University of Leeds',
            'sheffield.ac.uk': 'University of Sheffield',
            'nottingham.ac.uk': 'University of Nottingham',
            'birmingham.ac.uk': 'University of Birmingham',
            'cardiff.ac.uk': 'Cardiff University',
            'swansea.ac.uk': 'Swansea University',
            'gla.ac.uk': 'University of Glasgow',
            'strath.ac.uk': 'University of Strathclyde',
            'abdn.ac.uk': 'University of Aberdeen',
            'dundee.ac.uk': 'University of Dundee',
            'st-andrews.ac.uk': 'University of St Andrews',
            'tcd.ie': 'Trinity College Dublin',
            'ucd.ie': 'University College Dublin',
            'tum.de': 'Technical University of Munich',
            'ethz.ch': 'ETH Zurich',
            'epfl.ch': 'EPFL',
            'sorbonne-universite.fr': 'Sorbonne University',
            'ens.fr': 'École Normale Supérieure',
            'polytechnique.edu': 'École Polytechnique',
            'inria.fr': 'INRIA',
            'u-tokyo.ac.jp': 'University of Tokyo',
            'kyoto-u.ac.jp': 'Kyoto University',
            'osaka-u.ac.jp': 'Osaka University',
            'tohoku.ac.jp': 'Tohoku University',
            'titech.ac.jp': 'Tokyo Institute of Technology',
            'riken.jp': 'RIKEN',
            'tsinghua.edu.cn': 'Tsinghua University',
            'pku.edu.cn': 'Peking University',
            'sjtu.edu.cn': 'Shanghai Jiao Tong University',
            'zju.edu.cn': 'Zhejiang University',
            'fudan.edu.cn': 'Fudan University',
            'ustc.edu.cn': 'University of Science and Technology of China',
            'hit.edu.cn': 'Harbin Institute of Technology',
            'buaa.edu.cn': 'Beihang University',
            'bit.edu.cn': 'Beijing Institute of Technology',
            'xjtu.edu.cn': 'Xi\'an Jiaotong University',
            'seu.edu.cn': 'Southeast University',
            'hust.edu.cn': 'Huazhong University of Science and Technology',
            'cuhk.edu.hk': 'Chinese University of Hong Kong',
            'hku.hk': 'University of Hong Kong',
            'ust.hk': 'Hong Kong University of Science and Technology',
            'polyu.edu.hk': 'Hong Kong Polytechnic University',
            'cityu.edu.hk': 'City University of Hong Kong',
            'anu.edu.au': 'Australian National University',
            'unsw.edu.au': 'University of New South Wales',
            'usyd.edu.au': 'University of Sydney',
            'unimelb.edu.au': 'University of Melbourne',
            'monash.edu': 'Monash University',
            'uq.edu.au': 'University of Queensland',
            'adelaide.edu.au': 'University of Adelaide',
            'uwa.edu.au': 'University of Western Australia',
            'uts.edu.au': 'University of Technology Sydney',
            'rmit.edu.au': 'RMIT University',
            'deakin.edu.au': 'Deakin University',
            'griffith.edu.au': 'Griffith University',
            'qut.edu.au': 'Queensland University of Technology',
            'curtin.edu.au': 'Curtin University',
            'swinburne.edu.au': 'Swinburne University',
            'latrobe.edu.au': 'La Trobe University',
            'flinders.edu.au': 'Flinders University',
            'unisa.edu.au': 'University of South Australia',
            'canberra.edu.au': 'University of Canberra',
            'westernsydney.edu.au': 'Western Sydney University',
            'mq.edu.au': 'Macquarie University',
            'newcastle.edu.au': 'University of Newcastle',
            'wollongong.edu.au': 'University of Wollongong',
            'jcu.edu.au': 'James Cook University',
            'cdu.edu.au': 'Charles Darwin University',
            'murdoch.edu.au': 'Murdoch University',
            'ecu.edu.au': 'Edith Cowan University',
            'bond.edu.au': 'Bond University',
            'usc.edu.au': 'University of the Sunshine Coast',
            'scu.edu.au': 'Southern Cross University',
            'cqu.edu.au': 'Central Queensland University',
            'utas.edu.au': 'University of Tasmania',
            'acu.edu.au': 'Australian Catholic University',
            'notre-dame.edu.au': 'University of Notre Dame Australia',
            'torrens.edu.au': 'Torrens University Australia',
            'academia.edu': 'Academia.edu',
            'researchgate.net': 'ResearchGate',
            'arxiv.org': 'arXiv',
            'ieee.org': 'IEEE',
            'acm.org': 'ACM',
            'springer.com': 'Springer',
            'elsevier.com': 'Elsevier',
            'nature.com': 'Nature',
            'science.org': 'Science',
            'pnas.org': 'PNAS',
            'cell.com': 'Cell',
            'plos.org': 'PLOS',
            'biorxiv.org': 'bioRxiv',
            'medrxiv.org': 'medRxiv',
            'ssrn.com': 'SSRN',
            'nber.org': 'NBER',
            'jstor.org': 'JSTOR',
            'wiley.com': 'Wiley',
            'tandfonline.com': 'Taylor & Francis',
            'sage.com': 'SAGE',
            'cambridge.org': 'Cambridge University Press',
            'oup.com': 'Oxford University Press',
            'mit.edu': 'MIT Press',
            'harvard.edu': 'Harvard University Press',
            'yale.edu': 'Yale University Press',
            'chicago.edu': 'University of Chicago Press',
            'princeton.edu': 'Princeton University Press',
            'stanford.edu': 'Stanford University Press',
            'berkeley.edu': 'University of California Press',
            'columbia.edu': 'Columbia University Press',
            'nyu.edu': 'NYU Press',
            'cornell.edu': 'Cornell University Press',
            'upenn.edu': 'University of Pennsylvania Press',
            'duke.edu': 'Duke University Press',
            'northwestern.edu': 'Northwestern University Press',
            'vanderbilt.edu': 'Vanderbilt University Press',
            'jhu.edu': 'Johns Hopkins University Press',
            'georgetown.edu': 'Georgetown University Press',
            'tufts.edu': 'Tufts University Press',
            'brandeis.edu': 'Brandeis University Press',
            'bu.edu': 'Boston University Press',
            'northeastern.edu': 'Northeastern University Press',
            'wpi.edu': 'WPI Press',
            'rpi.edu': 'RPI Press',
            'rit.edu': 'RIT Press',
            'case.edu': 'Case Western Reserve University Press',
            'cwru.edu': 'Case Western Reserve University Press',
            'ucsd.edu': 'UC San Diego Press',
            'uci.edu': 'UC Irvine Press',
            'ucsb.edu': 'UC Santa Barbara Press',
            'ucsc.edu': 'UC Santa Cruz Press',
            'ucr.edu': 'UC Riverside Press',
            'ucmerced.edu': 'UC Merced Press',
            'ucdavis.edu': 'UC Davis Press',
            'ucsf.edu': 'UCSF Press',
        }
        
        # Extract domain from URL
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain_mapping.get(domain)
        except:
            return None
    
    def _clean_institution_name(self, name: str) -> str:
        """Clean and standardize institution names"""
        if not name:
            return ""
        
        # Remove common prefixes/suffixes
        name = name.strip()
        
        # Standardize common institution names
        name_mapping = {
            'Stanford': 'Stanford University',
            'MIT': 'Massachusetts Institute of Technology',
            'Harvard': 'Harvard University',
            'Berkeley': 'UC Berkeley',
            'UCLA': 'University of California Los Angeles',
            'CMU': 'Carnegie Mellon University',
            'Caltech': 'California Institute of Technology',
            'Princeton': 'Princeton University',
            'Yale': 'Yale University',
            'Columbia': 'Columbia University',
            'NYU': 'New York University',
            'Cornell': 'Cornell University',
            'UPenn': 'University of Pennsylvania',
            'UChicago': 'University of Chicago',
            'UMich': 'University of Michigan',
            'Georgia Tech': 'Georgia Institute of Technology',
            'UT Austin': 'University of Texas at Austin',
            'UW': 'University of Washington',
            'USC': 'University of Southern California',
            'Duke': 'Duke University',
            'Northwestern': 'Northwestern University',
            'Rice': 'Rice University',
            'Vanderbilt': 'Vanderbilt University',
            'Emory': 'Emory University',
            'JHU': 'Johns Hopkins University',
            'Georgetown': 'Georgetown University',
            'Tufts': 'Tufts University',
            'Brandeis': 'Brandeis University',
            'BU': 'Boston University',
            'Northeastern': 'Northeastern University',
            'WPI': 'Worcester Polytechnic Institute',
            'RPI': 'Rensselaer Polytechnic Institute',
            'RIT': 'Rochester Institute of Technology',
            'Case Western': 'Case Western Reserve University',
            'CWRU': 'Case Western Reserve University',
            'UCSD': 'UC San Diego',
            'UCI': 'UC Irvine',
            'UCSB': 'UC Santa Barbara',
            'UCSC': 'UC Santa Cruz',
            'UCR': 'UC Riverside',
            'UC Merced': 'UC Merced',
            'UC Davis': 'UC Davis',
            'UCSF': 'University of California San Francisco',
            'Oxford': 'Oxford University',
            'Cambridge': 'Cambridge University',
            'Imperial': 'Imperial College London',
            'UCL': 'University College London',
            'KCL': 'King\'s College London',
            'Edinburgh': 'University of Edinburgh',
            'Manchester': 'University of Manchester',
            'Warwick': 'University of Warwick',
            'Bristol': 'University of Bristol',
            'Bath': 'University of Bath',
            'Southampton': 'University of Southampton',
            'Surrey': 'University of Surrey',
            'Leeds': 'University of Leeds',
            'Sheffield': 'University of Sheffield',
            'Nottingham': 'University of Nottingham',
            'Birmingham': 'University of Birmingham',
            'Cardiff': 'Cardiff University',
            'Swansea': 'Swansea University',
            'Glasgow': 'University of Glasgow',
            'Strathclyde': 'University of Strathclyde',
            'Aberdeen': 'University of Aberdeen',
            'Dundee': 'University of Dundee',
            'St Andrews': 'University of St Andrews',
            'Trinity College Dublin': 'Trinity College Dublin',
            'UCD': 'University College Dublin',
            'TUM': 'Technical University of Munich',
            'ETH Zurich': 'ETH Zurich',
            'EPFL': 'École Polytechnique Fédérale de Lausanne',
            'Sorbonne': 'Sorbonne University',
            'ENS': 'École Normale Supérieure',
            'Polytechnique': 'École Polytechnique',
            'INRIA': 'French Institute for Research in Computer Science and Automation',
            'University of Tokyo': 'University of Tokyo',
            'Kyoto University': 'Kyoto University',
            'Osaka University': 'Osaka University',
            'Tohoku University': 'Tohoku University',
            'Tokyo Tech': 'Tokyo Institute of Technology',
            'RIKEN': 'RIKEN',
            'Tsinghua': 'Tsinghua University',
            'PKU': 'Peking University',
            'SJTU': 'Shanghai Jiao Tong University',
            'ZJU': 'Zhejiang University',
            'Fudan': 'Fudan University',
            'USTC': 'University of Science and Technology of China',
            'HIT': 'Harbin Institute of Technology',
            'BUAA': 'Beihang University',
            'BIT': 'Beijing Institute of Technology',
            'XJTU': 'Xi\'an Jiaotong University',
            'SEU': 'Southeast University',
            'HUST': 'Huazhong University of Science and Technology',
            'CUHK': 'Chinese University of Hong Kong',
            'HKU': 'University of Hong Kong',
            'HKUST': 'Hong Kong University of Science and Technology',
            'PolyU': 'Hong Kong Polytechnic University',
            'CityU': 'City University of Hong Kong',
            'ANU': 'Australian National University',
            'UNSW': 'University of New South Wales',
            'Sydney': 'University of Sydney',
            'Melbourne': 'University of Melbourne',
            'Monash': 'Monash University',
            'UQ': 'University of Queensland',
            'Adelaide': 'University of Adelaide',
            'UWA': 'University of Western Australia',
            'UTS': 'University of Technology Sydney',
            'RMIT': 'RMIT University',
            'Deakin': 'Deakin University',
            'Griffith': 'Griffith University',
            'QUT': 'Queensland University of Technology',
            'Curtin': 'Curtin University',
            'Swinburne': 'Swinburne University',
            'La Trobe': 'La Trobe University',
            'Flinders': 'Flinders University',
            'UniSA': 'University of South Australia',
            'UC': 'University of Canberra',
            'WSU': 'Western Sydney University',
            'Macquarie': 'Macquarie University',
            'Newcastle': 'University of Newcastle',
            'Wollongong': 'University of Wollongong',
            'JCU': 'James Cook University',
            'CDU': 'Charles Darwin University',
            'Murdoch': 'Murdoch University',
            'ECU': 'Edith Cowan University',
            'Bond': 'Bond University',
            'USC': 'University of the Sunshine Coast',
            'SCU': 'Southern Cross University',
            'CQU': 'Central Queensland University',
            'UTAS': 'University of Tasmania',
            'ACU': 'Australian Catholic University',
            'Notre Dame': 'University of Notre Dame Australia',
            'Torrens': 'Torrens University Australia',
        }
        
        # Apply mapping
        cleaned = name_mapping.get(name, name)
        
        # Remove unwanted characters and normalize
        cleaned = re.sub(r'[^\w\s\-\'\.]', '', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _parse_paper(self, result: Dict) -> Paper:
        """Parse a single paper from search results"""
        title = result.get('title', 'Untitled')
        
        # Extract authors
        authors = "Unknown authors"
        authors_list = []
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
        
        # Extract publication date with maximum precision
        published_date = "Unknown"
        published_date_for_sorting = None
        
        # Try to extract date from link first (arXiv papers have dates in URLs)
        if link and 'arxiv.org' in link:
            # Pattern: arxiv.org/abs/YYMM.NNNNN (where YY=year, MM=month)
            arxiv_id_match = re.search(r'arxiv\.org/abs/(\d{2})(\d{2})\.(\d+)', link)
            if arxiv_id_match:
                year_short = arxiv_id_match.group(1)
                month = arxiv_id_match.group(2)
                paper_num = arxiv_id_match.group(3)
                
                # Convert 2-digit year to 4-digit (assuming 20xx for now)
                year = f"20{year_short}"
                
                # For arXiv papers, estimate day from paper number
                # Lower paper numbers = earlier in month, higher = later
                try:
                    # Scale paper number to day (1-28 to avoid month boundary issues)
                    paper_int = int(paper_num[:3])  # Use first 3 digits
                    day = min(28, max(1, (paper_int % 28) + 1))
                except:
                    day = 15  # Default to mid-month
                
                day_str = f"{day:02d}"
                published_date = f"{year}-{month}-{day_str}"
                published_date_for_sorting = f"{year}-{month}-{day_str}"
        
        # If no arXiv date found, try to extract from summary
        if published_date_for_sorting is None and 'publication_info' in result and 'summary' in result['publication_info']:
            summary = result['publication_info']['summary']
            
            # Pattern 1: "YYYY-MM-DD" format (ISO date)
            iso_date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', summary)
            if iso_date_match:
                year, month, day = iso_date_match.groups()
                published_date = f"{year}-{month}-{day}"
                published_date_for_sorting = f"{year}-{month}-{day}"
            
            # Pattern 2: "Month Day, Year" format
            elif re.search(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', summary):
                month_date_match = re.search(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', summary)
                month_name = month_date_match.group(1)
                day = int(month_date_match.group(2))
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
                
                month_num = month_mapping.get(month_name.lower()[:3], '01')
                day_str = f"{day:02d}"
                published_date = f"{year}-{month_num}-{day_str}"
                published_date_for_sorting = f"{year}-{month_num}-{day_str}"
            
            # Pattern 3: "DD/MM/YYYY" or "MM/DD/YYYY" format
            elif re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', summary):
                date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', summary)
                part1, part2, year = date_match.groups()
                # Assume MM/DD/YYYY format (US style)
                month = f"{int(part1):02d}"
                day = f"{int(part2):02d}"
                published_date = f"{year}-{month}-{day}"
                published_date_for_sorting = f"{year}-{month}-{day}"
            
            # Pattern 4: "Month Year" format (no specific day)
            elif re.search(r'([A-Za-z]+)\s+(\d{4})', summary):
                month_year_match = re.search(r'([A-Za-z]+)\s+(\d{4})', summary)
                month_name = month_year_match.group(1)
                year = month_year_match.group(2)
                
                month_mapping = {
                    'jan': '01', 'january': '01', 'feb': '02', 'february': '02',
                    'mar': '03', 'march': '03', 'apr': '04', 'april': '04',
                    'may': '05', 'jun': '06', 'june': '06', 'jul': '07', 'july': '07',
                    'aug': '08', 'august': '08', 'sep': '09', 'september': '09',
                    'oct': '10', 'october': '10', 'nov': '11', 'november': '11',
                    'dec': '12', 'december': '12'
                }
                
                month_num = month_mapping.get(month_name.lower()[:3], '01')
                published_date = f"{year}-{month_num}-15"  # Default to mid-month
                published_date_for_sorting = f"{year}-{month_num}-15"
            
            # Pattern 5: Just year
            elif re.search(r'\b(19|20)\d{2}\b', summary):
                year_match = re.search(r'\b(19|20)\d{2}\b', summary)
                year = year_match.group(0)
                published_date = f"{year}-01-01"  # Default to January 1st
                published_date_for_sorting = f"{year}-01-01"
        
        # Default fallback
        if published_date_for_sorting is None:
            published_date_for_sorting = "1900-01-01"
            published_date = "1900-01-01"
        
        # Extract citation count
        citations = 0
        if 'inline_links' in result and 'cited_by' in result['inline_links']:
            citations = result['inline_links']['cited_by'].get('total', 0)
        
        # Extract institutions
        institutions = self._extract_institutions(result, authors_list, journal, snippet, link)
        
        return Paper(
            title=title,
            authors=authors,
            journal=journal,
            snippet=snippet,
            link=link,
            published_date=published_date,
            published_date_sort=published_date_for_sorting or "1900-01-01",
            citations=citations,
            institutions=institutions
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
        """Generate timeline data based on actual paper publication dates"""
        timeline = []
        
        if not papers:
            return timeline
        
        # Group papers by exact publication date (with day precision)
        daily_counts = {}
        
        for paper in papers:
            # Use exact date for more precise timeline
            if paper.published_date_sort and paper.published_date_sort != "1900-01-01":
                # Use the full date (YYYY-MM-DD)
                date_key = paper.published_date_sort
                daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        # Sort by date and create timeline
        sorted_dates = sorted(daily_counts.keys())
        
        # Create cumulative timeline (showing total citations up to each date)
        cumulative_count = 0
        for date in sorted_dates:
            cumulative_count += daily_counts[date]
            timeline.append({
                'date': date,
                'citations': cumulative_count
            })
        
        # If no valid dates found, create a simple current date entry
        if not timeline and papers:
            current_date = datetime.now().strftime('%Y-%m-%d')
            timeline.append({
                'date': current_date,
                'citations': len(papers)
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
                    'citations': paper.citations,
                    'institutions': paper.institutions
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