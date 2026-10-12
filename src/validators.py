import jsonschema
from jsonschema import validate
def verify_Json(data):
    schema = {
        "type" : "object",
        "properties" : {
            "response" : {
                "type" : "object",
                "properties" : {
                    "reviews" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object",
                            "properties" : {
                                "review": {"type": "string"}
                            },
                            "required" : ["review"]
                        }
                    }
                },
                "required" : ["reviews"]
            }
        },
        "required" : ["response"]
    }

    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False
    