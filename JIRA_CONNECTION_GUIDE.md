# How to Connect to Jira

This guide provides step-by-step instructions for connecting the Jira AI Assistant to your Jira instance.

## Prerequisites

- Jira Cloud account with administrator access
- Active Jira project where tickets will be created
- API access permissions in Jira

## Step 1: Generate Jira API Token

### For Jira Cloud:

1. **Log in to your Atlassian account**
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click **Create API token**

2. **Create the token**
   - Label: `Jira AI Assistant` (or any descriptive name)
   - Click **Create**
   - **Important:** Copy the token immediately as it won't be shown again

3. **Verify permissions**
   - Ensure your account has:
     - Browse Projects permission
     - Create Issues permission
     - Assign Issues permission
     - Edit Issues permission

### For Jira Server/Data Center:

1. Go to **Administration > System > REST API Browser**
2. Generate an API token through your user profile settings
3. Ensure REST API access is enabled in **Administration > System > Advanced Settings**

## Step 2: Gather Required Information

You'll need the following information:

- **Jira URL**: Your Jira instance URL (e.g., `https://your-domain.atlassian.net`)
- **Email**: The email address associated with your Jira account
- **API Token**: The token generated in Step 1
- **Project Key**: The key of your target project (e.g., `PROJ`, `DEV`, etc.)

### Finding Your Project Key:

1. Navigate to your Jira project
2. Look at the project URL or project settings
3. The project key appears in URLs like `https://your-domain.atlassian.net/browse/PROJ-123`
4. Or go to **Project Settings > Details** to find the key

## Step 3: Configure Environment Variables

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file** and update the Jira configuration:

   ```env
   # Jira Configuration
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your_jira_api_token_here
   JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
   ```

### Environment Variable Details:

| Variable | Description | Example |
|----------|-------------|---------|
| `JIRA_URL` | Your Jira instance URL | `https://company.atlassian.net` |
| `JIRA_EMAIL` | Your Jira account email | `user@company.com` |
| `JIRA_API_TOKEN` | API token from Step 1 | `ATATT3xFfGF0...` |
| `JIRA_PROJECT_KEY` | Target project key | `PROJ` |

## Step 4: Test the Connection

### Method 1: Using the API Documentation

1. **Start the backend services:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Access the API documentation:**
   - Open http://localhost:8000/api/docs
   - Look for the Jira connection test endpoint

### Method 2: Manual Test with Python

Create a test script to verify the connection:

```python
import requests
from requests.auth import HTTPBasicAuth

# Your configuration
JIRA_URL = "https://your-domain.atlassian.net"
JIRA_EMAIL = "your-email@example.com"
JIRA_API_TOKEN = "your-api-token"
PROJECT_KEY = "YOUR_PROJECT_KEY"

# Test API connection
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json"}

# Test basic connectivity
response = requests.get(
    f"{JIRA_URL}/rest/api/3/myself",
    headers=headers,
    auth=auth
)

if response.status_code == 200:
    print("✅ Connection successful!")
    print(f"Connected as: {response.json()['displayName']}")
else:
    print(f"❌ Connection failed: {response.status_code}")
    print(response.text)

# Test project access
response = requests.get(
    f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}",
    headers=headers,
    auth=auth
)

if response.status_code == 200:
    print(f"✅ Project '{PROJECT_KEY}' accessible!")
    print(f"Project name: {response.json()['name']}")
else:
    print(f"❌ Project access failed: {response.status_code}")
```

## Step 5: Verify Required Permissions

Ensure your Jira account has the following permissions for the target project:

### Required Permissions:
- **Browse Projects** - View project and issues
- **Create Issues** - Create new tickets
- **Assign Issues** - Assign tickets to users
- **Edit Issues** - Modify ticket details
- **Add Comments** - Add comments to tickets
- **View Development Tools** - Access development panel (if using)

### Checking Permissions:
1. Go to **Project Settings > Permissions**
2. Look for your user/group in the permission scheme
3. Verify all required permissions are granted

## Step 6: Configure Additional Settings (Optional)

### Custom Fields Configuration:
If your project uses custom fields, you may need to configure them in the application:

1. **Identify custom field IDs:**
   ```bash
   # Get all fields for your project
   curl -u "email:api_token" \
     "https://your-domain.atlassian.net/rest/api/3/field"
   ```

2. **Update configuration** if needed (check application documentation)

### Issue Types Configuration:
Ensure your project supports the issue types the AI assistant will create:
- Story
- Task
- Bug
- Sub-task

## Troubleshooting

### Common Issues and Solutions:

#### 1. Authentication Failed (401 Error)
- **Cause**: Incorrect email or API token
- **Solution**: Verify credentials, regenerate API token if needed

#### 2. Project Not Found (404 Error)
- **Cause**: Incorrect project key or insufficient permissions
- **Solution**: Verify project key and permissions

#### 3. Forbidden (403 Error)
- **Cause**: Insufficient permissions for the operation
- **Solution**: Check user permissions in Jira project settings

#### 4. Rate Limiting (429 Error)
- **Cause**: Too many API requests
- **Solution**: Wait and retry, consider implementing rate limiting

#### 5. SSL Certificate Issues
- **Cause**: Self-signed certificates (Jira Server)
- **Solution**: Configure SSL verification settings

### Testing Commands:

```bash
# Test basic connectivity
curl -u "email:api_token" \
  "https://your-domain.atlassian.net/rest/api/3/myself"

# Test project access
curl -u "email:api_token" \
  "https://your-domain.atlassian.net/rest/api/3/project/PROJ"

# Test issue creation (dry run)
curl -u "email:api_token" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"fields":{"summary":"Test","description":"Test issue","issuetype":{"name":"Task"},"project":{"key":"PROJ"}}}' \
  "https://your-domain.atlassian.net/rest/api/3/issue"
```

## Security Best Practices

1. **API Token Security:**
   - Store API tokens securely in environment variables
   - Never commit API tokens to version control
   - Rotate tokens regularly
   - Use separate tokens for different applications

2. **Access Control:**
   - Use a dedicated service account for the AI assistant
   - Grant minimum required permissions only
   - Monitor API usage and access logs

3. **Network Security:**
   - Use HTTPS for all API communications
   - Consider IP whitelisting if supported
   - Monitor for unusual API activity

## Next Steps

Once Jira connection is established:

1. **Test ticket creation** through the application
2. **Verify AI integration** with your Jira workflows
3. **Configure notification settings** if needed
4. **Set up monitoring** for API usage and errors
5. **Train team members** on using the AI assistant

## Support

If you encounter issues:

1. Check the [Jira API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
2. Review the application logs for detailed error messages
3. Verify all configuration values are correct
4. Test with a fresh API token if authentication issues persist

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Compatible with:** Jira Cloud, Jira Server/Data Center
