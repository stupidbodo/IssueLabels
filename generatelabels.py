import json
import base64
import urllib, urllib2
from getpass import getpass

# add/remove as needed.
# colors in hex without #
ISSUE_LABELS = {'bug':'CD2626',
                'feature':'31B94D',
                'todo':'FA9300',
                'rejected':'404040', 
                'blocking':'548CA8', 
                '!':'FFCC11',
                }

class GitHubIssue(object):

    def __init__(self, username, password, repository, organization=None):
        self.username = username
        self.password = password
        self.repository = repository
        self.organization_name = organization

    def create_label(self, name, color):
        data = json.dumps({'name': name, 'color': color})
        repo_username = self.organization_name if self.organization_name else self.username
        url = "https://api.github.com/repos/%s/%s/labels" % (repo_username, self.repository)
        
        api_response = self.call_api(url, data)
        if api_response:
            if api_response.getcode() == 200:
                print "New Label : %s" % name
                return True

        return False

    def call_api(self, url, data):
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'application/json')

        auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (self.username, self.password))
        request.add_header('Authorization', auth)

        if data:
            request.add_data(data)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return

        return response

# get information            
username = raw_input("Please enter GitHub Username: ")
password = getpass("Please enter GitHub Password: ")
organization = raw_input("Please enter GitHub Organization ( or leave blank ): ")
repository = raw_input("Please enter GitHub Repo name: ")

# setup for api call
issue = GitHubIssue(username, password, repository, organization)

# create labels
for label, color in ISSUE_LABELS.items():
    issue.create_label(label, color)