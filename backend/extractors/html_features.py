import requests
from bs4 import BeautifulSoup
import re

def get_html_features(url: str, url_domain: str = None) -> dict:
    """
    Extract features from the HTML content of the webpage based on structural characteristics
    and cross-site indicators.
    """
    features = {
        'has_form': 0,
        'has_password_field': 0,
        'has_hidden_inputs': 0,
        'has_external_action_form': 0,
        'num_iframes': 0,
        'num_script_tags': 0,
        'ratio_external_links': 0.0,
        'has_suspicious_title': 0,
        'page_size_kb': 0.0,
    }
    
    try:
        # Fetch with a short timeout to prevent hanging, spoof user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return features
            
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        features['page_size_kb'] = len(html_content) / 1024.0
        
        # Forms
        forms = soup.find_all('form')
        features['has_form'] = 1 if forms else 0
        
        for form in forms:
            # Check for password fields
            if form.find('input', type='password'):
                features['has_password_field'] = 1
            
            # Check if form action submits to a different domain
            action = form.get('action', '').lower()
            if action.startswith('http') and url_domain and url_domain not in action:
                features['has_external_action_form'] = 1
                
        # Hidden elements
        hidden_inputs = soup.find_all('input', type='hidden')
        features['has_hidden_inputs'] = 1 if len(hidden_inputs) > 3 else 0
        
        # Structure elements
        features['num_iframes'] = len(soup.find_all('iframe'))
        features['num_script_tags'] = len(soup.find_all('script'))
        
        # Link analysis (External vs Internal)
        links = soup.find_all('a', href=True)
        total_links = len(links)
        if total_links > 0 and url_domain:
            external_links = sum(1 for link in links if link['href'].startswith('http') and url_domain not in link['href'])
            features['ratio_external_links'] = external_links / total_links
            
        # Title analysis
        title = soup.title.string.lower() if soup.title else ''
        suspicious_words = ['login', 'signin', 'verify', 'update', 'account', 'secure', 'billing', 'support']
        if any(word in title for word in suspicious_words):
            features['has_suspicious_title'] = 1
            
    except Exception as e:
        # Silently fail for unreachable URLs or parsing errors
        # Typical for real-time systems to fallback to URL-only features
        pass
        
    return features
