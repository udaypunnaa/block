#!/usr/bin/env python3
"""
Test script for Google Safe Browsing API integration
Run this script to verify your API key is working correctly
"""

import sys
import os

try:
    from config import (GOOGLE_SAFE_BROWSING_API_KEY, SAFE_BROWSING_API_URL, 
                       CLIENT_ID, CLIENT_VERSION, THREAT_TYPES, 
                       PLATFORM_TYPE, THREAT_ENTRY_TYPE, API_TIMEOUT)
    import requests
    import json
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have:")
    print("1. Created config.py from config.example.py")
    print("2. Installed required packages: pip install requests")
    sys.exit(1)

def test_api_configuration():
    """Test if API is properly configured"""
    print("🔍 Testing Google Safe Browsing API Configuration...")
    print("=" * 50)
    
    # Check if API key is configured
    if GOOGLE_SAFE_BROWSING_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ ERROR: API key not configured!")
        print("   Please update config.py with your actual API key.")
        print("   See API_SETUP_INSTRUCTIONS.md for help.")
        return False
    
    print(f"✅ API Key configured (length: {len(GOOGLE_SAFE_BROWSING_API_KEY)})")
    print(f"✅ Client ID: {CLIENT_ID}")
    print(f"✅ Client Version: {CLIENT_VERSION}")
    print(f"✅ Threat Types: {len(THREAT_TYPES)} types configured")
    
    return True

def test_api_request(url):
    """Test API request with a given URL"""
    print(f"\n🌐 Testing URL: {url}")
    print("-" * 30)
    
    try:
        # Prepare API request
        api_url = f"{SAFE_BROWSING_API_URL}?key={GOOGLE_SAFE_BROWSING_API_KEY}"
        
        # Create request payload
        payload = {
            "client": {
                "clientId": CLIENT_ID,
                "clientVersion": CLIENT_VERSION
            },
            "threatInfo": {
                "threatTypes": THREAT_TYPES,
                "platformTypes": [PLATFORM_TYPE],
                "threatEntryTypes": [THREAT_ENTRY_TYPE],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }
        
        # Make API request
        headers = {
            'Content-Type': 'application/json'
        }
        
        print("📤 Sending request to API...")
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=API_TIMEOUT
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if matches found (malicious)
            if "matches" in result and result["matches"]:
                threat_types = [match["threatType"] for match in result["matches"]]
                print(f"⚠️  MALICIOUS: Threat types detected: {', '.join(threat_types)}")
                return True, f"Malicious website detected! Threat types: {', '.join(threat_types)}"
            else:
                print("✅ SAFE: No threats detected")
                return True, "The website is safe."
        
        elif response.status_code == 400:
            print("❌ ERROR: Invalid API request")
            return False, "Invalid API request. Please check the URL format."
        elif response.status_code == 401:
            print("❌ ERROR: Invalid API key")
            return False, "Invalid API key. Update your key in config.py"
        elif response.status_code == 429:
            print("❌ ERROR: Rate limit exceeded")
            return False, "Daily API limit reached. Try again later."
        else:
            print(f"❌ ERROR: Unexpected status code: {response.status_code}")
            return False, f"API request failed with status code: {response.status_code}"
    
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timeout")
        return False, "Error connecting to Safe Browsing API. Request timed out."
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Connection error")
        return False, "Error connecting to Safe Browsing API. Please check your internet connection."
    except Exception as e:
        print(f"❌ ERROR: Unexpected error: {str(e)}")
        return False, f"Unexpected error: {str(e)}"

def main():
    """Main test function"""
    print("🛡️  Google Safe Browsing API Test")
    print("=" * 50)
    
    # Test configuration
    if not test_api_configuration():
        return
    
    print("\n🧪 Running API Tests...")
    
    # Test URLs (Google's official test URLs)
    test_urls = [
        "http://testsafebrowsing.appspot.com/s/malware.html",  # Should be flagged as malware
        "https://www.google.com",  # Should be safe
        "http://malware.testing.google.test/testing/malware/",  # Should be flagged as malware
    ]
    
    success_count = 0
    total_tests = len(test_urls)
    
    for url in test_urls:
        try:
            success, message = test_api_request(url)
            if success:
                success_count += 1
        except Exception as e:
            print(f"❌ Test failed for {url}: {e}")
    
    print(f"\n📊 Test Results:")
    print(f"✅ Successful tests: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Your API integration is working correctly.")
        print("\n💡 You can now use the 'Check Malicious Status' feature in the main application.")
    else:
        print("⚠️  Some tests failed. Please check your configuration and internet connection.")
    
    print("\n📚 For more information, see API_SETUP_INSTRUCTIONS.md")

if __name__ == "__main__":
    main()
