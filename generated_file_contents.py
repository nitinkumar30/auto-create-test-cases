# File content templates for the generated files
import json
import random
from faker import Faker


class GeneratedFileContents:
    @staticmethod
    def config_properties(base_url, auth_token, timeout, env, log_level):
        return f"""base_url = {base_url}
auth_token = {auth_token}
timeout = {timeout}
log_level = {log_level}
env = {env}
"""

    @staticmethod
    def config_reader():
        return '''\
import os

class ConfigReader:
    def __init__(self, config_path="config/config.properties"):
        self.config = {}
        self._load_config(config_path)

    def _load_config(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    self.config[key.strip()] = value.strip()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_base_url(self):
        return self.get("base_url")

    def get_token(self):
        return self.get("auth_token")

    def get_timeout(self):
        return int(self.get("timeout", 10))

    def get_log_level(self):
        return self.get("log_level", "INFO")

    def get_env(self):
        return self.get("env", "dev")
'''

    @staticmethod
    def utils():
        return '''\
import logging
from config.config_reader import ConfigReader

cfg = ConfigReader()

def get_logger(name="api_test"):
    log_level = cfg.get_log_level().upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(numeric_level)
    return logger

def get_auth_headers():
    token = cfg.get("auth_token", "")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def merge_headers(defaults, extras):
    headers = defaults.copy()
    headers.update(extras)
    return headers
'''

    @staticmethod
    def requirements():
        return '''pyyaml
                  behave
                  requests
                '''

    @staticmethod
    def sample_feature_file():
        return '''\
Feature: Example API Test

  Scenario: Retrieve available pets
    Given I have the petstore API endpoint "/pet/findByStatus"
    And I set query parameter "status" to "available"
    When I send a GET request
    Then the response code should be 200
    And the response should contain a list of pets
'''

    @staticmethod
    def sample_step_definitions():
        # Creating reusable step definitions
        return '''\
from behave import given, when, then
import requests
# from ...core.utils import get_logger, get_auth_headers
# from ...config.config_reader import ConfigReader
from core.utils import get_logger, get_auth_headers
from config.config_reader import ConfigReader

logger = get_logger()
cfg = ConfigReader()

# Reusable step for setting up the API endpoint
@given('I have the API endpoint "{endpoint}"')
def step_given_endpoint(context, endpoint):
    context.url = cfg.get_base_url() + endpoint
    context.params = {}

# Reusable step for setting query parameters
@given('I set query parameter "{key}" to "{value}"')
def step_given_query_param(context, key, value):
    context.params[key] = value

# Reusable step for setting request body
@given('I send the request body with required data')
def step_given_request_body(context):
    # Placeholder - should be customized per endpoint
    context.body = {"key": "value"}

# Reusable step for sending a request
@when('I send a {method} request')
def step_when_send_request(context, method):
    headers = get_auth_headers()
    
    if method.upper() == "POST" and not hasattr(context, "body"):
    context.body = generate_post_payload(method.lower())
    if method.upper() == "PUT" and not hasattr(context, "body"):
    context.body = generate_put_payload(method.lower())

    if method.upper() == "GET":
        response = requests.get(context.url, headers=headers, params=context.params)
    elif method.upper() == "POST":
        response = requests.post(context.url, headers=headers, json=context.body, params=context.params)
    elif method.upper() == "PUT":
        response = requests.put(context.url, headers=headers, json=context.body, params=context.params)
    elif method.upper() == "PATCH":
        response = requests.patch(context.url, headers=headers, json=context.body, params=context.params)
    elif method.upper() == "DELETE":
        response = requests.delete(context.url, headers=headers, params=context.params)
    context.response = response
    logger.info(f"{method} {context.url} returned {response.status_code}")

# Reusable step for validating the response status code
@then('the response code should be {status_code:d}')
def step_then_status_code(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"
'''


fake = Faker()


def generate_post_payload(request_type="post"):
    """
    Generate JSON payload for POST or PUT requests using random data and write to a file.

    Args:
        request_type (str): "post" or "put"

    Returns:
        dict: The generated JSON payload
    """
    payload = {
        "id": random.randint(1, 1000),
        "name": fake.first_name(),
        "category": {
            "id": random.randint(1, 10),
            "name": random.choice(["Dogs", "Cats", "Birds", "Reptiles"])
        },
        "photoUrls": [
            fake.image_url()
        ],
        "tags": [
            {
                "id": random.randint(0, 50),
                "name": fake.word()
            }
        ],
        "status": random.choice(["available", "pending", "sold"])
    }

    filename = f"{request_type.lower()}_payload.json"
    with open(filename, "w") as f:
        json.dump(payload, f, indent=4)

    print(f"{request_type.upper()} payload written to {filename}")
    return payload


def generate_put_payload(request_type="put"):
    """
    Generate JSON payload for POST or PUT requests using random data and write to a file.

    Args:
        request_type (str): "post" or "put"

    Returns:
        dict: The generated JSON payload
    """
    payload = {
        "id": random.randint(1, 1000),
        "name": fake.first_name(),
        "category": {
            "id": random.randint(1, 10),
            "name": random.choice(["Dogs", "Cats", "Birds", "Reptiles"])
        },
        "photoUrls": [
            fake.image_url()
        ],
        "tags": [
            {
                "id": random.randint(0, 50),
                "name": fake.word()
            }
        ],
        "status": random.choice(["available", "pending", "sold"])
    }

    filename = f"{request_type.lower()}_payload.json"
    with open(filename, "w") as f:
        json.dump(payload, f, indent=4)

    print(f"{request_type.upper()} payload written to {filename}")
    return payload
