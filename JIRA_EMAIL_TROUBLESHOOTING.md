# Jira Email Address Troubleshooting

## Why Emails May Not Be Available

Jira Cloud often hides user email addresses due to:
1. **Privacy Settings** - Jira Cloud privacy controls
2. **API Permissions** - Your API token may not have permission to view emails
3. **GDPR Compliance** - Email addresses are considered personal data
4. **Organization Settings** - Admin-level privacy settings

## Check Your Jira Settings

### 1. Verify API Token Permissions
Your Jira API token inherits permissions from your user account:
- Go to https://id.atlassian.com/manage-profile/security/api-tokens
- Ensure the token is created by a user with proper permissions
- Ideally, use an admin account's API token

### 2. Check Jira Privacy Settings
1. Go to Jira → Settings (⚙️) → System
2. Navigate to **User management** → **User directory**
3. Check if "Show email addresses" is enabled

### 3. Organization Privacy Settings
1. Go to https://admin.atlassian.com/
2. Select your organization
3. Go to **Settings** → **Privacy**
4. Check email visibility settings

## What Happens When Emails Are Not Available

The system handles missing emails gracefully:

1. **Generates Placeholder Email**: `{accountId}@jira.local`
   - Example: `712020:1a6a8678-a71a-4e45-a1c2-bafef3bc876b@jira.local`

2. **Uses Account ID as Identifier**: The system uses Jira account ID as the primary identifier

3. **Functionality Still Works**: All features work without real emails:
   - ✅ Team sync
   - ✅ Capacity tracking
   - ✅ Assignment
   - ✅ Skills management

## Manual Email Update

If you know team members' emails, you can update them manually:

### Option 1: Via API
```bash
curl -X PUT http://localhost:8000/api/capacity/member/{username} \
  -H "Content-Type: application/json" \
  -d '{
    "username": "712020:1a6a8678-a71a-4e45-a1c2-bafef3bc876b",
    "email": "john.doe@company.com"
  }'
```

### Option 2: Via Database
```sql
UPDATE team_members 
SET email = 'john.doe@company.com' 
WHERE username = '712020:1a6a8678-a71a-4e45-a1c2-bafef3bc876b';
```

### Option 3: Via Edit Modal (Coming Soon)
We can add email field to the team member edit modal.

## Check Backend Logs

Look for warnings in the logs:

```bash
docker-compose -f Backend/docker-compose.dev.yml logs -f api | grep "Email not available"
```

You'll see messages like:
```
Email not available for user John Doe (712020:xxx). 
This may be due to Jira privacy settings or API permissions.
```

## Workarounds

### 1. Use Admin API Token
Create API token from a Jira admin account:
1. Log in as Jira admin
2. Go to https://id.atlassian.com/manage-profile/security/api-tokens
3. Create new token
4. Update `JIRA_API_TOKEN` in `.env`
5. Restart backend and re-sync

### 2. Request Organization Admin Access
Ask your Jira organization admin to:
1. Grant you admin permissions
2. Or enable email visibility in organization settings

### 3. Use Alternative Identifier
The system works fine with account IDs:
- Display names are still shown correctly
- All functionality works
- Only email field shows placeholder

## Testing Email Availability

Test if your API token can access emails:

```bash
# Replace with your credentials
JIRA_URL="https://your-domain.atlassian.net"
JIRA_EMAIL="your-email@example.com"
JIRA_TOKEN="your-api-token"

# Test API call
curl -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/3/user/search?query=" \
  | jq '.[0].emailAddress'
```

If you see `null` or the field is missing, emails are not accessible.

## Impact on Features

### ✅ Works Without Emails
- Team sync from Jira
- Capacity calculation
- Ticket assignment
- Skills management
- All core features

### ⚠️ Limited Without Emails
- Email notifications (if implemented)
- Email-based user lookup
- External integrations requiring email

## Recommended Solution

**Best Practice**: Use placeholder emails and focus on functionality
- The system is designed to work without real emails
- Account ID is the primary identifier
- Display names are shown in the UI
- Real emails are optional

## Future Enhancement

We can add an email field to the team member edit modal:
1. Sync team from Jira (gets account ID and display name)
2. Manually add emails via edit modal
3. Store in database
4. Use for notifications/integrations

Would you like me to implement this feature?

## Summary

**Don't worry if emails are not available!**
- ✅ System works perfectly without them
- ✅ Uses account ID as identifier
- ✅ Shows display names in UI
- ✅ All features functional
- ⚠️ Placeholder emails generated automatically

The missing emails are a Jira Cloud limitation, not a bug in our system.
