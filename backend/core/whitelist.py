import urllib.parse
import tldextract

# List of trusted high-authority domains
TRUSTED_DOMAINS = {
    'google.com',
    'www.google.com',
    'accounts.google.com',
    'mail.google.com',
    'drive.google.com',
    'apple.com',
    'www.apple.com',
    'icloud.com',
    'microsoft.com',
    'www.microsoft.com',
    'live.com',
    'outlook.com',
    'amazon.com',
    'www.amazon.com',
    'facebook.com',
    'www.facebook.com',
    'instagram.com',
    'www.instagram.com',
    'netflix.com',
    'www.netflix.com',
    'paypal.com',
    'www.paypal.com',
    'linkedin.com',
    'www.linkedin.com',
    'twitter.com',
    'x.com',
    'github.com',
    'www.github.com'
}

def is_whitelisted(url: str) -> bool:
    """
    Check if a URL belongs to a trusted domain.
    """
    try:
        # Normalize URL
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.netloc.lower()
        
        # Remove common prefixes like 'www.' for direct matching if needed
        # but the list already has them for precision.
        
        # Exact match check
        if hostname in TRUSTED_DOMAINS:
            return True
            
        # Extract registered domain for broader check
        ext = tldextract.extract(url)
        registered_domain = f"{ext.domain}.{ext.suffix}"
        
        if registered_domain in TRUSTED_DOMAINS:
            return True
            
        return False
    except Exception:
        return False
