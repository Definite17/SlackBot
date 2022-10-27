import json
import zenduty
from dateutil import parser

import Tokens


class ZendutyClient:
    def __init__(self, options):
        self.options = options
        self.client = zenduty.IncidentsApi(
            zenduty.ApiClient(self.options['zenduty_key']))

    # GET ALL INCIDENTS
    def get_all_incidents(self):
        body = {
            'page': 1,
            'status': 1,
            'team_id': [Tokens.TEAM_ID],
            'service_ids': [],
            'user_ids': []
        }
        # CALLS API TO GET ALL INCIDENTS
        response = self.client.get_incidents(body)
        return response

    # GET INCIDENTS BY NUMBER

    def get_incident_by_number(self, incident_number):
        response = self.client.get_incidents_by_number(incident_number)
        return response
