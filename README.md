# Malicious Website Blocker

A GUI application built with Python Tkinter to block and unblock websites by modifying the system's hosts file.

## Features

- **Block Single Websites**: Enter a URL and block it instantly
- **Bulk Block**: Upload a text or CSV file with multiple URLs to block them all at once
- **Unblock Single Websites**: Remove a website from the blocked list
- **Bulk Unblock**: Upload a file with URLs to unblock multiple websites
- **Email Verification**: All block/unblock operations require email verification for security
- **Random Password Generation**: Cryptographically secure verification codes
- **Project Information**: View application details and usage instructions
- **Clean UI**: Modern interface with yellow, blue, and red color scheme

## Requirements

- Python 3.6 or higher
- Windows (tested), Linux, or macOS
- Administrator/root privileges (required to modify hosts file)

## Installation

1. Clone or download the files to a directory (e.g., `C:\block\`)
2. Ensure Python is installed on your system
3. No additional packages required (uses only built-in libraries)
4. **Configure Email Settings**: See [Email Setup Instructions](email_setup_instructions.md)

## Email Verification Setup

**⚠️ IMPORTANT: Email verification is required for all block/unblock operations.**

Before using the application, you must configure email settings:

1. Open `malicious_website_blocker.py`
2. Update lines 15-17 with your email credentials:
   ```python
   SENDER_EMAIL = "your.email@gmail.com"     # Your Gmail address
   SENDER_PASSWORD = "your-app-password"      # Gmail app password
   RECEIVER_EMAIL = "your.email@gmail.com"   # Same email (you receive codes)
   ```

3. **For Gmail users**:
   - Enable 2-Factor Authentication
   - Generate an app password
   - Use the app password (not your regular password)

4. **For detailed setup instructions**: See [email_setup_instructions.md](email_setup_instructions.md)

## Usage

### Method 1: Direct Run (Recommended)
```bash
python run_as_admin.py
```
This will automatically request administrator privileges if needed.

### Method 2: Manual Admin Run
1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the application directory
3. Run: `python malicious_website_blocker.py`

## How It Works

The application modifies your system's hosts file located at:
- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/macOS**: `/etc/hosts`

When you block a website:
- The URL is normalized (removes www., protocols)
- Entries are added redirecting the domain to `127.0.0.1` (localhost)
- Both `domain.com` and `www.domain.com` variants are blocked

## File Formats for Bulk Operations

Create a text file (`.txt`) or CSV file (`.csv`) with one URL per line:

```
# Comments start with #
example.com
malicious-site.net
phishing-domain.org
suspicious-website.com
```

## UI Components

### Header Section
- **Yellow Logo**: Application identifier
- **Title**: "Block Malicious Websites"
- **Project Info Button**: Click to view application information

### Block Websites Section
- **URL Input**: Enter website to block
- **Upload File Button** (Yellow): Select file for bulk blocking
- **Block Button** (Red): Block the entered URL

### Unblock Websites Section  
- **URL Input**: Enter website to unblock
- **Upload File Button** (Yellow): Select file for bulk unblocking
- **Unblock Button** (Blue): Unblock the entered URL

## Safety Features

- **Duplicate Check**: Won't block already blocked sites
- **URL Validation**: Basic validation of entered URLs
- **Backup Handling**: Safe modification of hosts file
- **Error Reporting**: Clear feedback on operations
- **Threading**: Non-blocking UI during operations

## Important Notes

⚠️ **Administrator Rights Required**: The application needs elevated privileges to modify the hosts file.

⚠️ **Backup Recommended**: Consider backing up your hosts file before making changes.

⚠️ **System Impact**: Blocked websites won't be accessible from this computer until unblocked.

## Troubleshooting

### "Permission Denied" Error
- Run the application as Administrator (Windows) or with sudo (Linux/macOS)
- Use the `run_as_admin.py` launcher script

### Website Still Accessible After Blocking
- Clear your browser cache and DNS cache
- Windows: Run `ipconfig /flushdns` in Command Prompt
- Some browsers may use their own DNS resolution

### File Upload Not Working
- Ensure the file is in plain text format
- Check that URLs are separated by newlines
- Verify file permissions

## Files Included

- `malicious_website_blocker.py` - Main application with email verification
- `run_as_admin.py` - Admin privilege launcher
- `sample_urls.txt` - Example URLs file for testing
- `email_setup_instructions.md` - Detailed email configuration guide
- `README.md` - This documentation

## Version History

**v1.0.0**
- Initial release
- Basic block/unblock functionality
- Bulk operations support
- Clean Tkinter GUI
- Cross-platform compatibility

## License

© 2024 Website Security Tools. All rights reserved.

## Support

For issues or questions, ensure you're running with appropriate system privileges and that your hosts file is not write-protected.
