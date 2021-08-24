# rbacv1

You will need your ShiftLeft ORG ID and Access Token (personal access token not CI token)

The users defined in the CSV should be verified users, either through email invite or SSO provisioning. 

The teams can be new, the script can create new teams from the CSV.

You will also need to ensure you are following the correct CSV format, see example rbac.csv (case sensitive)

If a user is a Super Admin, you cannot update their org role with this method.
