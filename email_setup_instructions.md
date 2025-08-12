# Email Configuration Setup

To enable email verification in the Malicious Website Blocker, you need to configure your email credentials.

## Gmail Setup (Recommended)

### 1. Enable 2-Factor Authentication
1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to "Security" → "2-Step Verification"
3. Follow the setup process to enable 2FA

### 2. Generate App Password
1. After enabling 2FA, go to "Security" → "App passwords"
2. Select "Mail" as the app and "Windows Computer" as the device
3. Click "Generate" and copy the 16-character password

### 3. Update Configuration
Open `malicious_website_blocker.py` and update these lines (around line 15-17):

```python
# Email Configuration - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
SENDER_EMAIL = "your.email@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = "your-app-password"    # Replace with your app password
RECEIVER_EMAIL = "your.email@gmail.com"  # Same as sender (you receive codes)
```

**Example:**
```python
SENDER_EMAIL = "myapp2024@gmail.com"
SENDER_PASSWORD = "abcd efgh ijkl mnop"  # 16-character app password
RECEIVER_EMAIL = "myapp2024@gmail.com"   # Same email receives verification codes
```

## Configuration Details

### SENDER_EMAIL
- Your Gmail address that will send verification emails
- Must have 2FA enabled and app password generated

### SENDER_PASSWORD
- The 16-character app password from Google (not your regular password)
- Format: "abcd efgh ijkl mnop" (with spaces)

### RECEIVER_EMAIL
- Fixed admin email address that receives verification codes
- Can be the same as SENDER_EMAIL or different
- User cannot change this at runtime (security feature)

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never share your app password** - treat it like a regular password
2. **Use a dedicated Gmail account** for the application if possible
3. **The receiver email is hardcoded** - this is intentional for security
4. **App passwords bypass 2FA** - only use them for trusted applications

## Testing Email Setup

1. Update the configuration with your credentials
2. Run the application
3. Try to block a website (e.g., "example.com")
4. Check that you receive the verification email
5. Enter the code to complete the test

## Troubleshooting

### "Failed to send verification email" Error

**Common causes:**
- Incorrect email/password combination
- 2FA not enabled on Gmail account
- App password not generated
- Blocked by Gmail security settings
- Network/firewall issues

**Solutions:**
1. Double-check email and app password
2. Ensure 2FA is enabled on your Google account
3. Generate a new app password
4. Try with a different Gmail account
5. Check your network connection

### "Authentication failed" Error
- Make sure you're using the app password, not your regular password
- Verify 2FA is enabled on the sender Gmail account

### Emails not received
- Check spam/junk folder
- Verify RECEIVER_EMAIL is correct
- Try sending a test email manually to the receiver address

## Alternative Email Providers

While Gmail is recommended, you can modify the SMTP settings for other providers:

### Outlook/Hotmail
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

### Yahoo Mail
```python
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

**Note:** Other providers may have different authentication requirements.
