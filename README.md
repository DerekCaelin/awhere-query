# awhere-query
A simple script to query the aWhere database.

You'll need to create a file called "credentials.py" and add the following lines:
headers = {
    'authorization': "Basic [your base64 encoded credentials]",
    'content-type': "application/x-www-form-urlencoded"
    }
    
More details on how to get credentials here: http://developer.awhere.com/api/authentication
A sample base64 encoder: https://www.base64encode.org
