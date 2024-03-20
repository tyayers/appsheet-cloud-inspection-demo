import base64
import logging
import pprint
import io
import datetime

import google.auth

from google.auth.transport.requests import AuthorizedSession
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

creds, project = google.auth.default(
  scopes=[
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/drive.readonly",
  ]
)


def getImagePrompt(image, prompt1):
    authed_session = AuthorizedSession(creds)

    a = datetime.datetime.now()

    vertexai.init(project=project, location="us-central1")
    model = GenerativeModel("gemini-1.0-pro-vision-001")

    image1 = Part.from_data(data=base64.b64decode(image), mime_type="image/png")

    responses = model.generate_content(
      [image1, prompt1],
      generation_config={
          "max_output_tokens": 2048,
          "temperature": 0.4,
          "top_p": 1,
          "top_k": 32
      },
      safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      },
      stream=True,
    )
    
    result = ""
    for response in responses:
      result = result + response.text

    # response = authed_session.post(
    #   url="https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models/imagetext:predict".format(
    #     project=project
    #   ),
    #   json={
    #     "instances": [
    #         {
    #             "prompt": prompt1,
    #             "image": {"bytesBase64Encoded": image},
    #         }
    #     ],
    #     "parameters": {"sampleCount": 1},
    #   },
    # )
    b = datetime.datetime.now()
    c = b - a
    logging.error(
        "{s} ms to q&a prompt with GenAI Vision service.".format(
            s=c.total_seconds() * 1000
        )
    )
    return result


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
    logging.error(
        "{s} ms to caption with GenAI Vision service.".format(
            s=c.total_seconds() * 1000
        )
    )

    return response.content


def convertImageToBase64(topic, image):
    imageResult = ""

    if "_Images/" in image:
        logging.error("Retrieving Google Drive image: " + image)

        a = datetime.datetime.now()
        imageResult = getImageFromDrive(image.split("/")[-1])
        b = datetime.datetime.now()
        c = b - a

        logging.error(
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
    else:
        imageResult = image

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

    files = response.get("files", [])

    if len(files) > 0:
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
    else:
        encoded_string = "error"

    return encoded_string
