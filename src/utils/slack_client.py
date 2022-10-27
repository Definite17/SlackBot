from slack_bolt import App
import json
import zenduty
from dateutil import parser

import logging
import Tokens
from src.utils import view_dict
from src.utils.zenduty_api_client import ZendutyApiClient
from src.utils.zenduty_client import ZendutyClient

logger = logging.getLogger()

app = App(
    token=Tokens.SLACK_BOT_TOKEN,
    signing_secret=Tokens.SIGNING_SECRET
)


def get_app():
    return app


zenduty_api_options = {'zenduty_api_key': Tokens.ZENDUTY_API_KEY}
zenduty_api_client = ZendutyApiClient(zenduty_api_options)

zenduty_option = {'zenduty_key': Tokens.ZENDUTY_API_KEY}
zenduty_client = ZendutyClient(zenduty_option)


# BOT Mention - Demo
@app.event("app_mention")
def event_test(body, say):
    user = body['event']['user']
    say(f"What's up? <@{user}>!")


# GET-ALL-INCIDENTS SLASH COMMAND
@app.command("/get-all-incidents")
def handle_get_all_incidents_command(ack, body, say):
    ack()
    response = zenduty_client.get_all_incidents()
    response_dict = json.loads(response.data.decode("utf-8").replace("'", '"'))
    body = {
        'page': 1,
        'status': 1,
        'team_id': [Tokens.TEAM_ID],
        'service_ids': [],
        'user_ids': []
    }

    total_no_of_incidents = response_dict['count']
    say(
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"SHOWING RECENT 10 INCIDENTS\n",
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": f"Total number of incidents: {total_no_of_incidents}",
                        "type": "mrkdwn"
                    }
                ]
            },
        ]
    )

    # LOOP THROUGH INCIDENTS
    for current in range(10):
        # INCREMENTS PAGE NUMBER
        body['page'] = body['page'] + 1
        # response = self.client.get_incidents(body)
        response_dict = json.loads(
            response.data.decode("utf-8").replace("'", '"'))

        # INCIDENT NUMBER
        incidentNumber = response_dict['results'][current]['incident_number']

        # INCIDENT TITLE
        title = response_dict['results'][current]['title']
        # INCIDENT URL
        incidentURL = "https://zenduty.com/dashboard/incidents/" + \
            str(incidentNumber)

        # SUMMARY
        summary = response_dict['results'][current]['summary']

        # SERVICE DATA
        serviceName = response_dict['results'][current]['service_object']['name']
        serviceId = response_dict['results'][current]['service_object']['unique_id']
        teamId = response_dict['results'][current]['service_object']['team']
        serviceURL = "https://www.zenduty.com/dashboard/teams/" + \
            teamId + "/services/" + serviceId

        # ESCALATION POLICY DATA
        escalationPolicyName = response_dict['results'][current]['escalation_policy_object']['name']

        # ASSIGNED TO DATA
        assignedToName = response_dict['results'][current]['assigned_to_name']
        assignedToId = response_dict['results'][current]['assigned_to']
        assignedToURL = "https://zenduty.com/dashboard/users/" + assignedToId

        # PARSING STATUS
        if response_dict['results'][current]['status'] == 1:
            status = "Triggered"
        elif response_dict['results'][current]['status'] == 2:
            status = "Acknowledged"
        elif response_dict['results'][current]['status'] == 3:
            status = "Resolved"

        # PARSING URGENCY
        if response_dict['results'][current]['urgency'] == 0:
            urgency = "Low"
        elif response_dict['results'][current]['urgency'] == 1:
            urgency = "High"

        # PARSING DATETIME FORMAT FROM RFC3339
        crDate = parser.isoparse(
            response_dict['results'][current]['creation_date'])
        creationDate = (
            f"{crDate.year}/{crDate.month}/{crDate.day} at {crDate.hour}:{crDate.minute} UTC")

        try:
            ackDate = parser.isoparse(
                response_dict['results'][current]['acknowledged_date'])
            acknowledgedDate = (
                f"{ackDate.year}/{ackDate.month}/{ackDate.day} at {ackDate.hour}:{ackDate.minute} UTC")
        except:
            acknowledgedDate = response_dict['results'][current]['acknowledged_date']

        try:
            resDate = parser.isoparse(
                response_dict['results'][current]['resolved_date'])
            resolvedDate = (
                f"{resDate.year}/{resDate.month}/{resDate.day} at {resDate.hour}:{resDate.minute} UTC")
        except:
            resolvedDate = response_dict['results'][current]['resolved_date']

        # SENDS INCIDENT INFO TO SLACK
        say(
            text=f"*INCIDENT DETAILS*\n",
            blocks=[
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": f"{title}\n"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                            {
                                "text": f"Click <{incidentURL}|here> to view incident on Zenduty\n"
                                        f"*_Incident Number:_* {incidentNumber}\n",
                                "type": "mrkdwn"
                            }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": f"*Summary:*\n> {summary}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": f"*Service:* <{serviceURL}|{serviceName}>\n"
                                    f"*Escalation Policy:* {escalationPolicyName}\n"
                                    f"*Assigned To:* <{assignedToURL}|{assignedToName}>\n"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": f"*Status:* {status}\n"
                                    f"*Urgency:* {urgency}\n"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": f"*Created at:* {creationDate}\n"
                                    f"*Acknowledged at:* {acknowledgedDate}\n"
                                    f"*Resolved at:* {resolvedDate}\n"
                    }
                },
            ]
        )
        # INCREMENTS CURRENT LIST INDEX
        current += 1


# GET-INCIDENT-BY-NUMBER SLASH COMMAND
@app.command("/get-incident-by-number")
def handle_get_incidents_by_number_command(ack, body, say):
    ack()
    # SLICES NUMBER AFTER SLASH COMMAND
    incident_number = body['text']
    response = zenduty_client.get_incident_by_number(incident_number)

    # CONVERTING BYTES TO DICTIONARY
    response_dict = json.loads(response.data.decode("utf-8").replace("'", '"'))
    # CHECKS FOR ITS TYPE AND NATURAL NUMBER
    if incident_number.isnumeric() and int(incident_number) > 0:
        # GETS INCIDENT DETAILS FROM ZENDUTY API
        response = response
        # CONVERTING BYTES TO DICTIONARY
        response_dict = json.loads(
            response.data.decode("utf-8").replace("'", '"'))

        # INCIDENT NUMBER
        incidentNumber = response_dict['incident_number']

        # INCIDENT TITLE
        title = response_dict['title']
        # INCIDENT URL
        incidentURL = "https://zenduty.com/dashboard/incidents/" + incident_number

        # SUMMARY
        summary = response_dict['summary']

        # SERVICE DATA
        serviceName = response_dict['service_object']['name']
        serviceId = response_dict['service_object']['unique_id']
        teamId = response_dict['service_object']['team']
        serviceURL = "https://www.zenduty.com/dashboard/teams/" + \
            teamId + "/services/" + serviceId

        # ESCALATION POLICY DATA
        escalationPolicyName = response_dict['escalation_policy_object']['name']

        # ASSIGNED TO DATA
        assignedToName = response_dict['assigned_to_name']
        assignedToId = response_dict['assigned_to']
        assignedToURL = "https://zenduty.com/dashboard/users/" + assignedToId

        # PARSING STATUS
        if response_dict['status'] == 1:
            status = "Triggered"
        elif response_dict['status'] == 2:
            status = "Acknowledged"
        elif response_dict['status'] == 3:
            status = "Resolved"

        # PARSING URGENCY
        if response_dict['urgency'] == 0:
            urgency = "Low"
        elif response_dict['urgency'] == 1:
            urgency = "High"

        try:
            # PARSING DATETIME FORMAT FROM RFC3339
            crDate = parser.isoparse(response_dict['creation_date'])
            creationDate = (
                f"{crDate.year}/{crDate.month}/{crDate.day} at {crDate.hour}:{crDate.minute} UTC")

            try:
                ackDate = parser.isoparse(response_dict['acknowledged_date'])
                acknowledgedDate = (
                    f"{ackDate.year}/{ackDate.month}/{ackDate.day} at {ackDate.hour}:{ackDate.minute} UTC")
            except:
                acknowledgedDate = response_dict['acknowledged_date']

            try:
                resDate = parser.isoparse(response_dict['resolved_date'])
                resolvedDate = (
                    f"{resDate.year}/{resDate.month}/{resDate.day} at {resDate.hour}:{resDate.minute} UTC")
            except:
                resolvedDate = response_dict['resolved_date']

            # SENDING NECCESAARY DETAILS TO SLACK CHANNEL
            say(
                text=f"*INCIDENT DETAILS*\n",
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{title}\n"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "text": f"Click <{incidentURL}|here> to view incident on Zenduty\n"
                                        f"*_Incident Number:_* {incidentNumber}\n",
                                "type": "mrkdwn"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Summary:*\n> {summary}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Service:* <{serviceURL}|{serviceName}>\n"
                                    f"*Escalation Policy:* {escalationPolicyName}\n"
                                    f"*Assigned To:* <{assignedToURL}|{assignedToName}>\n"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Status:* {status}\n"
                                    f"*Urgency:* {urgency}\n"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Created at:* {creationDate}\n"
                                    f"*Acknowledged at:* {acknowledgedDate}\n"
                                    f"*Resolved at:* {resolvedDate}\n"
                        }
                    },
                ]
            )
        except:
            say(f"No data found for Incident Number: {incident_number}")
    else:
        say(f"This command only accepts NATURAL NUMBERS. Enter a valid NUMBER and Try Again!")

# Opening Modals using Shortcuts
@app.shortcut("open_modal")
def open_modal(ack, body, client):
    ack()

    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        view=view_dict.data
    )

# Opening Modals using Slash Commands
@app.command("/create-incident")
def command_check(ack, client, command):
    ack()

    client.views_open(
        trigger_id=command["trigger_id"],
        view=view_dict.data
    )

# Options - Escalation Policies
@app.options("escalation-policy-select-action")
def show_escalation(ack, payload):
    escalation_policy_list = zenduty_api_client.get_escalation_policies(Tokens.TEAM_ID)
    options = []
    for escalation_policy in escalation_policy_list:
        options.append({
            "text": {"type": "plain_text", "text": escalation_policy['name']},
            "value": escalation_policy['unique_id'],
        })

    ack(options=options)


# Options - Services
@app.options("service_select-action")
def show_Services(ack, payload):
    service_list = zenduty_api_client.get_services(Tokens.TEAM_ID)
    options = []
    for service in service_list:
        options.append({
            "text": {"type": "plain_text", "text": service['name']},
            "value": service['unique_id'],
        })
    ack(options=options)


# View Submission
@app.view("view_1")
def handle_view_events(ack, body, say):
    ack()
    info = list(body["view"]["state"]["values"].values())
    title = info[0]["title-action"]["value"]
    summary = info[1]["summary-action"]["value"]
    escalationPolicy = info[2]["escalation-policy-select-action"]["selected_option"]["value"]
    service = info[3]["service_select-action"]["selected_option"]["value"]
    incident_body = {
        "service": service,
        "escalation_policy": escalationPolicy,
        "title": title,
        "summary": summary}
    incident_number = zenduty_api_client.create_incident(incident_body)
    zenduty_client.get_incident_by_number(incident_number)
