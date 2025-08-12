# Google Safe Browsing API Setup Instructions

## Overview
The "Check Malicious Status" feature uses Google Safe Browsing API v4 to check if websites are malicious. This document explains how to set up and configure the API.

## Prerequisites
- Google Cloud Platform account
- Python 3.x with requests library

## Step 1: Get Google Safe Browsing API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Safe Browsing API:
   - Go to **APIs & Services** > **Library**
   - Search for "Safe Browsing API"
   - Click on "Safe Browsing API" and click **Enable**

4. Create credentials:
   - Go to **APIs & Services** > **Credentials**
   - Click **Create Credentials** > **API Key**
   - Copy the generated API key

5. (Optional) Restrict the API key:
   - Click on your API key to edit it
   - Under "API restrictions", select "Restrict key"
   - Choose "Safe Browsing API" from the list

## Step 2: Configure the Application

1. Open the `config.py` file in your project directory
2. Replace `YOUR_API_KEY_HERE` with your actual API key:
   ```python
   GOOGLE_SAFE_BROWSING_API_KEY = "your-actual-api-key-here"
   ```

## Step 3: API Usage Limits

- **Free Tier**: 10,000 requests per day
- **Rate Limit**: 100 requests per 100 seconds per user

For higher limits, you may need to enable billing on your Google Cloud project.

## Step 4: Testing the Feature

1. Run the application: `python malicious_website_blocker.py`
2. In the "Check Malicious Status" section, enter a URL (e.g., `malware.testing.google.test`)
3. Click "Check Malicious Status"
4. The application will query the API and show results

## How It Works

The feature performs the following steps:

1. **URL Validation**: Checks if the input is empty or placeholder text
2. **URL Formatting**: Adds `http://` if no protocol is specified
3. **API Request**: Sends the URL to Google Safe Browsing API v4
4. **Response Processing**:
   - If malicious → Shows confirmation dialog asking to block the site
   - If safe → Shows "The website is safe" message
   - If error → Shows appropriate error message
5. **Optional Blocking**: If user confirms, triggers the website blocking process

## API Request Structure

```json
{
  "client": {
    "clientId": "block-malicious-websites-tool",
    "clientVersion": "1.0"
  },
  "threatInfo": {
    "threatTypes": [
      "MALWARE",
      "SOCIAL_ENGINEERING", 
      "UNWANTED_SOFTWARE",
      "POTENTIALLY_HARMFUL_APPLICATION"
    ],
    "platformTypes": ["ANY_PLATFORM"],
    "threatEntryTypes": ["URL"],
    "threatEntries": [
      {"url": "http://example.com"}
    ]
  }
}
```

## Error Handling

The application handles various error scenarios:

- **API Key Not Configured**: Shows setup message
- **Invalid URL**: Shows URL format error
- **Network Issues**: Shows connection error
- **API Rate Limits**: Shows quota exceeded message
- **Invalid API Key**: Shows authentication error

## Security Notes

- Store your API key securely in the `config.py` file
- Do not commit your API key to version control
- Consider using environment variables for production deployments
- The API key has been added to `.gitignore` to prevent accidental commits

## Threat Types Detected

- **MALWARE**: Malicious software
- **SOCIAL_ENGINEERING**: Phishing and social engineering sites
- **UNWANTED_SOFTWARE**: Sites hosting unwanted software
- **POTENTIALLY_HARMFUL_APPLICATION**: Apps that may be harmful

## Testing URLs

Google provides test URLs for testing:
- Safe URL: `http://testsafebrowsing.appspot.com/s/phishing.html`
- Malware URL: `http://malware.testing.google.test/testing/malware/`
- Phishing URL: `http://testsafebrowsing.appspot.com/s/phishing.html`

## Troubleshooting

1. **"API key not configured" error**:
   - Make sure you've updated `config.py` with your API key

2. **"Invalid API key" error**:
   - Check that your API key is correct
   - Verify that Safe Browsing API is enabled in Google Cloud Console

3. **"Daily API limit reached" error**:
   - Wait for the quota to reset (24 hours)
   - Or upgrade your Google Cloud billing plan

4. **Connection errors**:
   - Check your internet connection
   - Verify firewall settings allow HTTPS requests

## Additional Resources

- [Google Safe Browsing API Documentation](https://developers.google.com/safe-browsing/v4)
- [API Reference](https://developers.google.com/safe-browsing/v4/reference/rest)
- [Google Cloud Console](https://console.cloud.google.com/)
