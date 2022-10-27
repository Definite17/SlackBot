import zenduty
from zenduty import ApiClient
import json
import logging

logger = logging.getLogger()


class ZendutyApiClient:
    def __init__(self, options):
        self.options = options
        self.api_client = ApiClient(self.options['zenduty_api_key'])
        self.incident_api_client = zenduty.IncidentsApi(self.api_client)

    def create_incident(self, request):
        response = self.incident_api_client.create_incident(request)
        response_dict = json.loads(
            response.data.decode("utf-8").replace("'", '"'))
        incident_number = response_dict['incident_number']
        return incident_number

    def get_escalation_policies(self, team_id):
        escalation_policy = self.api_client.call_api('GET',
                                                     '/api/account/teams/{}/escalation_policies/'.format(team_id))
        response_data = json.loads(
            escalation_policy.data.decode("utf-8").replace("'", '"'))

        response_list = []
        for policy in response_data:
            response_list.append({
                'name': policy['name'],
                'unique_id': policy['unique_id']
            })
        return response_list

    def get_services(self, team_id):
        service_client = zenduty.ServicesApi(self.api_client)
        response = service_client.get_service_for_team(team_id)

        response_data = json.loads(
            response.data.decode("utf-8").replace("'", '"'))

        response_list = []
        for policy in response_data:
            response_list.append({
                'name': policy['name'],
                'unique_id': policy['unique_id']
            })
        return response_list
