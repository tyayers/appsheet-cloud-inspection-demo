import pprint
from proto import fields
import web
import json
import logging
import urllib
import requests
import io
import os
import os.path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google.auth

from app_utils import convertImageToBase64, getImagePrompt, getImageCaption

topic = "car-parts"
topicDocs = "car-part-docs"

urls = ("/{topic}(.*)".format(topic=topic), "datahandler", 
        "/", "openapispec",
        "/{topicDocs}(.*)".format(topicDocs=topicDocs), "docshandler")
app = web.application(urls, globals())

if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(
        cred,
        {
            "projectId": cred.project_id,
        },
    )


class datahandler:
    db = firestore.client()

    # Returns all of the notes
    def GET(self, id):
        new_result = {}

        if len(id) == 0:
            forms_ref = self.db.collection(topic)
            forms = forms_ref.stream()
            new_result = {topic: []}

            for form in forms:
                new_result[topic].append(form.to_dict())
        else:
            doc_ref = self.db.collection(topic).document(id[1:])
            doc = doc_ref.get()
            new_result = doc.to_dict()

        if new_result:
            web.header("Content-Type", "application/json")
            return json.dumps(new_result)
        else:
            return web.notfound("Not found")

    # Posts a new object to be stored
    def POST(self, name):
        data = json.loads(web.data())
        try:
          imageData = convertImageToBase64(topic, data["image"])
        except:
          logging.error("Exception in loading image, image not loaded.")

        if imageData != "error":

            visionData = getImagePrompt(imageData, """please describe this car part in 2-3 technical words and not in a sentence.""")

            data["partName"] = visionData.replace(".", "").strip()

            # visionCaptionData = json.loads(getImageCaption(imageData))
            # if "predictions" in visionCaptionData:
            #   data["generatedCaption"] = (
            #     visionCaptionData["predictions"][0].capitalize() + "."
            #   )
        else:
          data["partName"] = "Not recognized."

        self.db.collection(topic).document(data["id"]).set(data)

        web.header("Content-Type", "application/json")
        return json.dumps(data)

    # Puts an object to be updated
    def PUT(self, name):
        data = json.loads(web.data())

        logging.info(json.dumps(data))

        self.db.collection(topic).document(data["id"]).set(data)

        pprint.pprint(data)

        web.header("Content-Type", "application/json")
        return json.dumps(data)

    # Deletes an object
    def DELETE(self, id):
        if id:
            self.db.collection(topic).document(id[1:]).delete()

        return "200 OK"


class docshandler:
    db = firestore.client()

    # Returns all of the notes
    def GET(self, id):
        new_result = {}

        if len(id) == 0:
            forms_ref = self.db.collection(topicDocs)
            forms = forms_ref.stream()
            new_result = {topicDocs: []}

            for form in forms:
                new_result[topicDocs].append(form.to_dict())
        else:
            doc_ref = self.db.collection(topicDocs).document(id[1:])
            doc = doc_ref.get()
            new_result = doc.to_dict()

        if new_result:
            web.header("Content-Type", "application/json")
            return json.dumps(new_result)
        else:
            return web.notfound("Not found")


# Returns the OpenAPI spec, filled in with the current server
class openapispec:
    # Returns the OpenAPI spec, filled in with the current server
    def GET(self):
        f = open("apispec.yaml", "r")
        spec = f.read()
        spec = spec.replace("SERVER_URL", web.ctx.home.replace("http://", "https://"))
        web.header("Content-Type", "text/plain;charset=UTF-8")
        return spec


if __name__ == "__main__":
    app.run()
