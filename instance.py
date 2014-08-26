import httplib2
import time

from apiclient.discovery import build as discovery_build
from json import dumps as json_dumps
from oauth2client.client import SignedJwtAssertionCredentials

CLIENT_SECRETS_FILE = 'client_secret.json'
CREDENTIALS_FILE = 'credentials.json'

SCOPE_SQLSERVICE = 'https://www.googleapis.com/auth/sqlservice.admin'
SCOPE_PLATFORM = 'https://www.googleapis.com/auth/cloud-platform'


def get_authenticated_service():
    credentials = SignedJwtAssertionCredentials(
        '270233216449-ncjv2h895qv8tu0aed5pgorka9l2vuil@developer.gserviceaccount.com',
        open('service_account_key.p12', 'rb').read(),
        scope=SCOPE_SQLSERVICE,
        token_uri='https://accounts.google.com/o/oauth2/token')

    http = credentials.authorize(httplib2.Http())
    return discovery_build('sqladmin', 'v1beta3', http=http)


def create_instance(service, instance, tier="D0"):
    req = service.instances().insert(project="titanpaas", body={"project": "titanpaas", "instance": instance, "settings": {"tier": tier}})
    resp = req.execute()

    req = service.operations().get(project="titanpaas", instance=instance, operation=resp['operation'])
    resp = req.execute()
    print json_dumps(resp, indent=2)
    for _ in range(60):
        req = service.operations().get(project="titanpaas", instance=instance, operation=resp['operation'])
        resp = req.execute()
        print json_dumps(resp, indent=2)
        if resp['state'] == 'DONE':
            break
        time.sleep(1)


def delete_instance(service, instance):
    req = service.instances().delete(project="titanpaas", instance=instance)
    resp = req.execute()


if __name__ == '__main__':
    service = get_authenticated_service()

    delete_instance(service, "mkwtest5")
    create_instance(service, "mkwtest6", tier="D2")
    req = service.instances().list(project='titanpaas')
    resp = req.execute()
    print json_dumps(resp, indent=2)
