import json
import os

from jsonschema import Draft4Validator, RefResolver, validate

from integration.main.request import RequestBuilder


class SchemaFile(object):

    @staticmethod
    def open(filename):
        with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
            content = json.load(file)
        return content


class Schemas(object):
    BASIC_METADATA = SchemaFile.open('metadata/basic_destructured_metadata.json')
    LOCALIZED_METADATA = SchemaFile.open('metadata/localized_en_metadata.json')
    OVERRIDDEN_PRODUCT_FIELDS = SchemaFile.open('overrides/overridden_product_fields.json')
    PURCHASE_PRODUCT = SchemaFile.open('purchase_product.json')
    TEST_ENVIRONMENT = SchemaFile.open('test_environment.json')

    @staticmethod
    def validate(value, schema):
        validate(value, schema)

    @staticmethod
    def swagger_validate(response, swagger_endpoint):
        url = response.request.url
        partitioned_url = url.split('/')
        protocol = partitioned_url[0]
        url_base = partitioned_url[2]
        gateway = partitioned_url[3]
        swagger_url = '{}//{}/{}/swagger.json'.format(protocol, url_base, gateway)

        swagger = RequestBuilder(swagger_url).get()
        swagger.assert_is_success()
        gateway_schema = swagger.content

        resolver = RefResolver(swagger_url, gateway_schema)
        validator = Draft4Validator(
            schema=gateway_schema['paths'][swagger_endpoint][response.request.method.lower()]['responses'][
                str(response.status)]['schema'],
            resolver=resolver
        )
        validator.validate(response.content)


class TCSShemas(object):

    @staticmethod
    def publish_title(reason, titleid, title_id, friendly_name, pgn, pop, code,
                      namespace_id, title_version_id, server_api_key, client_api_key):

        schema = {
            "title":
                {
                    "access":False,
                    "state":True,
                    "reason":reason,
                    "id":titleid,
                    "title_id":title_id,
                    "friendly_name":friendly_name,
                    "pgn":pgn,
                    "pop":pop,
                    "code":code,
                    "ggapi": {},
                    "webhook_gzip_accepted": False,
                    "automatic_registration": False,
                    "internal": False,
                    "external_product_cdn": False,
                    "enforce_prerequisites": False,
                    "event_schemas": {},
                    "document_schemas": {},
                    "namespaces": [
                        {
                            "id": namespace_id,
                            "title_id": title_id,
                            "key": "ru.temp6.players",
                            "entity_type_id": 0,
                            "full_title_id": titleid
                        }
                    ],
                    "title_versions": [
                        {
                            "id": title_version_id,
                            "name": "initial",
                            "active": True,
                            "server_api_key": server_api_key,
                            "client_api_key": client_api_key,
                            "allowed_client_apis": {},
                            "dependent_title_versions": [],
                            "default": True,
                            "catalogs_activations": []
                        }
                    ],
                    "title_permissions": {
                        "override": {},
                        "catalog": {},
                        "client_api": {
                            "api_list": [],
                            "white_list": False
                        },
                        "server_api": {
                            "api_list": [],
                            "white_list": False
                        }
                    },
                    "permitting_titles": [],
                    "shared_titles": [],
                    "title_group": "temp6",
                    "tags": [],
                    "branches": [
                        {
                            "title_code": code,
                            "branch_code": "MAIN",
                            "friendly_name": "Main branch",
                            "description": "Main branch",
                            "is_active": True,
                            "is_overlay": False,
                            "branch_name": "MAIN"
                        }
                    ],
                    "bulk_operations": [],
                    "next_schema_versions": {},
                    "public": False,
                    "type": "game"
                }
        }

        return schema
