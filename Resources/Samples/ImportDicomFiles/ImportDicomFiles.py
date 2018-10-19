#!/usr/bin/python

import sys
import os.path
import httplib2
import base64
import json
from sets import Set

if len(sys.argv) != 4 and len(sys.argv) != 6:
    print("""
Sample script to recursively import in Orthanc all the DICOM files
that are stored in some path. Please make sure that Orthanc is running
before starting this script. The files are uploaded through the REST
API.

Usage: %s [hostname] [HTTP port] [path]
Usage: %s [hostname] [HTTP port] [path] [username] [password]
For instance: %s localhost 8042 .
""" % (sys.argv[0], sys.argv[0], sys.argv[0]))
    exit(-1)

base_url = 'http://%s:%d' % (sys.argv[1], int(sys.argv[2]))
URL = base_url + '/instances'

processed = 0
success = 0
patients = Set()

sys.stdout.write("Importing to %s" % URL)


# This function will upload a single file to Orthanc through the REST API
def uploadFile(path):
    global processed
    global success
    global patients

    f = open(path, "rb")
    content = f.read()
    f.close()

    try:
        sys.stdout.write("Importing %s" % path)

        h = httplib2.Http()

        headers = {'content-type': 'application/dicom'}

        if len(sys.argv) == 6:
            username = sys.argv[4]
            password = sys.argv[5]

            # h.add_credentials(username, password)

            # This is a custom reimplementation of the
            # "Http.add_credentials()" method for Basic HTTP Access
            # Authentication (for some weird reason, this method does
            # not always work)
            # http://en.wikipedia.org/wiki/Basic_access_authentication
            headers['authorization'] = 'Basic ' + base64.b64encode(username + ':' + password)

        resp, content = h.request(URL, 'POST',
                                  body=content,
                                  headers=headers)

        if resp.status == 200:
            sys.stdout.write(" => success ")
            orthanc_response = json.loads(content)

            status = orthanc_response["Status"]

            processed += 1

            if status == "AlreadyStored":
                sys.stdout.write(" => already stored\n")
            else:
                sys.stdout.write(" => IMPORTED\n")
                success += 1

            instance_url = base_url + orthanc_response["Path"]
            inst_resp, inst_content = h.request(instance_url, 'GET', headers=headers)
            orthanc_instance = json.loads(inst_content)

            series_url = base_url + '/series/' + orthanc_instance["ParentSeries"]
            series_resp, series_content = h.request(series_url, 'GET', headers=headers)
            orthanc_series = json.loads(series_content)

            studies_url = base_url + '/studies/' + orthanc_series["ParentStudy"]
            studies_resp, studies_content = h.request(studies_url, 'GET', headers=headers)
            orthanc_study = json.loads(studies_content)

            patient_url = base_url + '/patients/' + orthanc_study["ParentPatient"]

            patients.add(patient_url)

        else:
            sys.stdout.write(" => failure (Is it a DICOM file?)\n")

    except:
        sys.stdout.write(" => unable to connect (Is Orthanc running? Is there a password?)\n")


if os.path.isfile(sys.argv[3]):
    # Upload a single file
    uploadFile(sys.argv[3])
else:
    # Recursively upload a directory
    for root, dirs, files in os.walk(sys.argv[3]):
        for f in files:
            if f.lower().endswith(('.jpg', '.dll', '.exe', '.pdf', '.jpeg', '.js', '.xsl', '.xml', '.html', '.htm',
                                   '.gif', '.css', '.ini', '.db', '.xls')):
                sys.stdout.write("NOT Importing %s\n" % os.path.join(root, f))
            else:
                uploadFile(os.path.join(root, f))

print("\nSummary: %d DICOM file(s) have been processed, %d have been imported" % (processed, success))
print("\nImported patients:\n")
for patient in patients:
    print patient
