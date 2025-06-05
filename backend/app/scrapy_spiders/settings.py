# Use a real browser User-Agent to reduce blocking
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

# Add a delay between requests to avoid hitting servers too fast
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True

# Obey robots.txt rules (set to False for testing)
ROBOTSTXT_OBEY = False

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [502, 503, 504, 408, 429]

# Allow all HTTP error codes to be processed
HTTPERROR_ALLOW_ALL = True

# Enable cookies
COOKIES_ENABLED = True

# Request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Log level
LOG_LEVEL = "INFO"

# Disable telnet console
TELNETCONSOLE_ENABLED = False

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
