import base64
import pprint
import io
import datetime

import google.auth

# import google.auth.transport.requests
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

creds, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
)


def getImagePrompt(image, prompt1):
    authed_session = AuthorizedSession(creds)

    a = datetime.datetime.now()
    response = authed_session.post(
        url="https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models/imagetext:predict".format(
            project=project
        ),
        json={
            "instances": [
                {
                    "prompt": prompt1,
                    "image": {"bytesBase64Encoded": image},
                }
            ],
            "parameters": {"sampleCount": 1},
        },
    )
    b = datetime.datetime.now()
    c = b - a
    pprint.pprint(
        "{s} ms to q&a prompt with GenAI Vision service.".format(
            s=c.total_seconds() * 1000
        )
    )
    return response.content


def getImageCaption(image):
    authed_session = AuthorizedSession(creds)

    a = datetime.datetime.now()
    response = authed_session.post(
        url="https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models/imagetext:predict".format(
            project=project
        ),
        json={
            "instances": [
                {
                    "image": {"bytesBase64Encoded": image},
                }
            ],
            "parameters": {"sampleCount": 1, "language": "en"},
        },
    )
    b = datetime.datetime.now()
    c = b - a
    pprint.pprint(
        "{s} ms to caption with GenAI Vision service.".format(
            s=c.total_seconds() * 1000
        )
    )

    return response.content


def convertImageToBase64(topic, image):
    imageResult = ""

    if image.startswith(topic + "_Images/"):
        a = datetime.datetime.now()
        imageResult = getImageFromDrive(image.split("/")[-1])
        b = datetime.datetime.now()
        c = b - a

        pprint.pprint(
            "{s} ms to get image from google drive.".format(s=c.total_seconds() * 1000)
        )
    elif image.startswith("data:image/png;base64,"):
        imageResult = image.replace("data:image/png;base64,", "")
        imageResult = imageResult.split("#filename=", 1)[0]
    elif image.startswith("data:image/jpeg;base64,"):
        imageResult = image.replace("data:image/jpeg;base64,", "")
        imageResult = imageResult.split("#filename=", 1)[0]
    elif image.startswith("data:image/jpg;base64,"):
        imageResult = image.replace("data:image/jpg;base64,", "")
        imageResult = imageResult.split("#filename=", 1)[0]

    return imageResult


def getImageFromDrive(name):
    service = build("drive", "v3", credentials=creds)
    page_token = None

    response = (
        service.files()
        .list(
            q="name='" + name + "'",
            spaces="drive",
            fields="nextPageToken, files(id, name, thumbnailLink)",
            pageToken=page_token,
        )
        .execute()
    )

    for file in response.get("files", []):
        # Process change
        print("Found file: " + file.get("name") + " and id: " + file.get("id"))
        request = service.files().get_media(fileId=file.get("id"))
        # fh = io.BytesIO()
        fh = io.FileIO("image.png", "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download " + str(int(status.progress() * 100)))

        # output["formThumbnail"] = file["thumbnailLink"]
        break

    with open("image.png", "rb") as imageFile:
        encoded_string = base64.b64encode(imageFile.read()).decode("utf-8")

    return encoded_string
