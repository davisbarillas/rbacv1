#!/usr/bin/env python3
import csv
import requests
from config import SHIFTLEFT_ORG_ID, SHIFTLEFT_ACCESS_TOKEN

def main():
    with requests.Session() as s:
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/teams'.format(SHIFTLEFT_ORG_ID)
        headers = {'Authorization':'Bearer {}'.format(SHIFTLEFT_ACCESS_TOKEN)}
        r = requests.get(url, headers=headers)
        teams = r.json()['response']
        #print(teams)
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/users'.format(SHIFTLEFT_ORG_ID)
        r = requests.get(url, headers=headers)
        users = r.json()['response']
        #print(users)
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/roles'.format(SHIFTLEFT_ORG_ID)
        r = requests.get(url, headers=headers)
        roles = r.json()['response']
        #print(roles)

        with open("rbac.csv", "r") as csv_file:
            csvreader = csv.DictReader(csv_file)

            csvlist = []
            for x in csvreader:
                csvlist.append(x)
                #print(csvlist)

            for row in csvlist:
                user_email = row.get('email')
                #useremail = next(dictionary for dictionary in users if dictionary["email"] == user_email)
                #userrealemail = useremail.get('id_v2')
                #print(userrealemail)
                #print(useremail)
                user_team = row.get('team')
                org_role = row.get('orgrole')
                team_role = row.get('teamrole')
                #print(row)
                #print(userid)

                for user in users:
                    if user_email in user.values():
                        user_id = user.get('id_v2')
                        user_org_role_payload = {"org_role": str(org_role)}
                        url = 'https://www.shiftleft.io/api/v4/orgs/{orgid}/rbac/users/{userid}'.format (orgid=SHIFTLEFT_ORG_ID, userid=user_id)
                        r = requests.put(url, headers=headers, json=user_org_role_payload)
                        orgupdate = 'Updated organization role for {email} to {orgrole}.'.format (email=user_email, orgrole=org_role)
                        print(orgupdate)
                        for team in teams:
                            if user_team in team.values():
                                user_team_id = team.get('team_id')
                                version = team.get('team_version')
                                payload = {
                                            "version": int(version),
                                                "add_team_membership": [
                                                    {
                                                        "user_id_v2": str(user_id),
                                                        "team_role": str(team_role)
                                                    }
                                                ]
                                            }
                                url = 'https://www.shiftleft.io/api/v4/orgs/{orgid}/rbac/teams/{userteam}'.format (orgid=SHIFTLEFT_ORG_ID, userteam=user_team_id)
                                r = requests.put(url, headers=headers, json=payload)
                                teamupdate = 'Updated team role for {email} to {teamrole}.'.format (email=user_email, teamrole=team_role)
                                print(teamupdate)
                                teamchange = 'Updated team for {email} to {team}.'.format (email=user_email, team=user_team)
                                print(teamchange)
                        else:
                                    team_payload = {
                                                    "name": str(user_team),
                                                        "team_membership": [
                                                            {
                                                                "user_id_v2": str(user_id),
                                                                "team_role": str(team_role)
                                                            }
                                                        ]
                                                    }
                                    url = 'https://www.shiftleft.io/api/v4/orgs/{orgid}/rbac/teams'.format (orgid=SHIFTLEFT_ORG_ID)
                                    r = requests.post(url, headers=headers, json=team_payload)
                                    #print(r.status_code)
                                    url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/teams'.format(SHIFTLEFT_ORG_ID)
                                    headers = {'Authorization':'Bearer {}'.format(SHIFTLEFT_ACCESS_TOKEN)}
                                    r = requests.get(url, headers=headers)
                                    teams = r.json()['response']
                                    #print(teams)
                                    #createteam = 'Created {teamname} and added user {email} to team.'.format (email=user_email, teamname=user_team)
                                    #print(createteam)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()