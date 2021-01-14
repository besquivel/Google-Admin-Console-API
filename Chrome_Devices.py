from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos','https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly']
chromebook_list = ['HP Chromebook x360 11 G2 EE','Dell Chromebook 11 2-in-1 (3189)','Dell Chromebook 3100 2-in-1',
                   'Dell Chromebook 11 (3120)','Dell Chromebook 11 (3180)','Dell Chromebook 13 (7310)','Chromebook x360 11 G3 EE'
                   ,'HP Chromebook 14','Dell Chromebook 3100']

def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    print('Getting All of the devices in the domain')
    activities = service.chromeosdevices()
    request = activities.list(customerId=os.environ.get('CLIENTID'),maxResults = 500, orderBy = 'status')
    count = 0
    while request is not None:

        activities_doc = request.execute()


        chromeosdevices = activities_doc.get('chromeosdevices', [])


        if not chromeosdevices:
            print('No devices in the domain.')
        else:
            print('Devices:')
            with open('Chromebook_list.csv','a') as outFile:

                for device in chromeosdevices:
                    try:
                        if device['model'] not in chromebook_list:
                            print(device['model'])
                            count = count + 1

                        else:
                            chromebook = (u'{0}, {1} , {2}'.format(device['serialNumber'],device['recentUsers'][0]['email'],device['activeTimeRanges'][-1]['date']))
                            print(chromebook)
                            outFile.write(chromebook + "\n")
                    except KeyError:
                        print(device)
                        count = count + 1
                        pass


        request = activities.list_next(request,activities_doc)
    print(count)




if __name__ == '__main__':
    main()
