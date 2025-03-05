import json


class ElementSelectors:
    def __init__(self, jsonElement: json):
        self.jsonElement = jsonElement

    def getElementInfo(self, element: str):
        return self.jsonElement[f"{element}"]

    def getSelector(self, element: str):
        return self.jsonElement[f"{element}"].get("selector")

    def getName(self, element: str):
        return self.jsonElement[f"{element}"].get("name")
