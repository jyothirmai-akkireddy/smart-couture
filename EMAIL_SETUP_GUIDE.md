# StyleSense AI - Email Configuration Guide

## 🎯 Overview
The forgot password feature requires email configuration to send OTP codes to users. This guide will help you set it up properly.

## ⚙️ Email Configuration Steps

### Option 1: Gmail (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Navigate to Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "StyleSense AI"
   - Click "Generate"
   - Copy the 16-character password (remove spaces)

3. **Set Environment Variables**

   **Linux/Mac:**
   ```bash
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-16-char-app-password"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-16-char-app-password
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:MAIL_USERNAME="your-email@gmail.com"
   $env:MAIL_PASSWORD="your-16-char-app-password"
   ```

4. **Permanent Configuration (.env file)**
   
   Create a `.env` file in the project root:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

   Make sure to load these in your app.py:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Option 2: Other Email Providers

**Outlook/Hotmail:**
```python
# In auth_routes.py, change:
server = smtplib.SMTP('smtp-mail.outlook.com', 587)
```

**Yahoo:**
```python
# In auth_routes.py, change:
server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
```

## 🧪 Testing

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Check console for confirmation:**
   ```
   📧 Attempting to send OTP email to user@example.com...
   ✅ OTP email sent successfully to user@example.com
   ```

3. **If you see errors:**
   ```
   ❌ Email credentials not configured
   Please set MAIL_USERNAME and MAIL_PASSWORD environment variables
   ```
   
   or
   
   ```
   ❌ Error sending email: ...
   ```

   Check:
   - Environment variables are set correctly
   - Using App Password (not regular password) for Gmail
   - 2FA is enabled for Gmail
   - No typos in email/password

## 🔒 Security Best Practices

1. **Never commit .env file to git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use App Passwords (not regular passwords)**
   - Gmail requires App Passwords when 2FA is enabled
   - More secure than using your actual password

3. **Restrict App Password scope**
   - Only grant "Mail" access
   - Revoke if compromised

## 📧 Email Template

The OTP email sent to users looks like this:

```
Subject: StyleSense AI - Password Reset OTP

Hello,

Your OTP for password reset is: 123456

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email and your password will remain unchanged.

Best regards,
StyleSense AI Team
```

## 🐛 Troubleshooting

### Issue: "Email service is not configured"
**Solution:** Set MAIL_USERNAME and MAIL_PASSWORD environment variables

### Issue: "Authentication failed"
**Solution:** 
- Use App Password instead of regular password
- Enable 2FA on Gmail account
- Check for typos in credentials

### Issue: "Connection timeout"
**Solution:**
- Check internet connection
- Verify SMTP server and port (Gmail: smtp.gmail.com:587)
- Check firewall settings

### Issue: "Email not received"
**Solution:**
- Check spam/junk folder
- Verify recipient email is correct
- Check email sending logs in console
- Test with different email address

## 📝 Production Deployment

### Heroku:
```bash
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
```

### AWS/DigitalOcean/VPS:
Add to your systemd service file or docker-compose:
```yaml
environment:
  - MAIL_USERNAME=your-email@gmail.com
  - MAIL_PASSWORD=your-app-password
```

### Docker:
```bash
docker run -e MAIL_USERNAME=your-email@gmail.com \
           -e MAIL_PASSWORD=your-app-password \
           your-image
```

## ✅ Verification Checklist

- [ ] Environment variables set correctly
- [ ] Gmail 2FA enabled (if using Gmail)
- [ ] App Password generated (if using Gmail)
- [ ] Application restarted after setting variables
- [ ] Test email sent successfully
- [ ] OTP received in inbox
- [ ] OTP verification works
- [ ] Password reset completes successfully

## 🎉 Success!

Once configured, users will:
1. Enter their email on forgot password page
2. Receive OTP via email within seconds
3. Enter OTP to verify identity
4. Reset their password successfully

No OTP will be displayed on the page - it's only sent via email for security!
