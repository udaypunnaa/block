# Configuration file for Website Blocker
# Store your API keys and other sensitive information here

# Google Safe Browsing API v4 Configuration
# Get your API key from: https://console.cloud.google.com/apis/credentials
GOOGLE_SAFE_BROWSING_API_KEY = "AIzaSyBp9q6ZEBq2mkNZv7BVUYe-SDMwkGbqlKs"

# Safe Browsing API Settings
SAFE_BROWSING_API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
CLIENT_ID = "block-malicious-websites-tool"
CLIENT_VERSION = "1.0"

# Threat types to check for
THREAT_TYPES = [
    "MALWARE",
    "SOCIAL_ENGINEERING", 
    "UNWANTED_SOFTWARE",
    "POTENTIALLY_HARMFUL_APPLICATION"
]

# Platform and entry types
PLATFORM_TYPE = "ANY_PLATFORM"
THREAT_ENTRY_TYPE = "URL"

# Request timeout in seconds
API_TIMEOUT = 10

# Cache settings (optional for future implementation)
CACHE_RESULTS = True
CACHE_DURATION_HOURS = 24
