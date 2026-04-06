import re
import urllib.parse
import tldextract

def get_url_features(url: str) -> dict:
    """
    Extract basic structural and lexical features from the URL.
    """
    # Ensure URL has a scheme for proper parsing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
        
    parsed = urllib.parse.urlparse(url)
    ext = tldextract.extract(url)
    
    features = {}
    
    # 1. URL Length
    features['url_length'] = len(url)
    # Phishing URLs often use long strings to obscure the actual domain
    features['is_long_url'] = 1 if len(url) > 75 else 0
    
    # 2. Domain Length
    domain = ext.domain + ('.' + ext.suffix if ext.suffix else '')
    features['domain_length'] = len(domain)
    
    # 3. Presence of IP Address in URL
    # Obscuring the domain using an IP instead of a hostname
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    features['has_ip_in_url'] = 1 if re.search(ip_pattern, parsed.netloc) else 0
    
    # 4. Use of Shortening Services
    shortening_services = ['bit.ly', 'goo.gl', 't.co', 'tinyurl', 'is.gd', 'cli.gs', 
                          'yfrog', 'migre.me', 'ff.im', 'tiny.cc', 'url4.eu', 'twit.ac', 
                          'su.pr', 'twurl.nl', 'snipurl.com', 'short.to', 'BudURL.com']
    features['is_shortened'] = 1 if any(service in domain for service in shortening_services) else 0
    
    # 5. Presence of '@' symbol
    # Browsers ignore everything before '@', phishers use it to hide the real domain
    features['has_at_symbol'] = 1 if '@' in url else 0
    
    # 6. Double Slash Redirect
    # Position of the last '//' can indicate redirection
    double_slash_pos = url.rfind('//')
    features['has_double_slash_redirect'] = 1 if double_slash_pos > 7 else 0
    
    # 7. Prefix or Suffix in Domain
    features['has_dash_in_domain'] = 1 if '-' in domain else 0
    
    # 8. Subdomains
    subdomain_count = len(ext.subdomain.split('.')) if ext.subdomain else 0
    features['subdomain_count'] = subdomain_count
    
    # 9. HTTPS Token in Domain
    features['https_token_in_domain'] = 1 if 'https' in domain else 0
    
    # 10. Suspicious Characters
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slash'] = url.count('/')
    features['num_question_marks'] = url.count('?')
    features['num_equals'] = url.count('=')
    
    return features
