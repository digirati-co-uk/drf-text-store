import pytest
import requests
from tests.utils import is_responsive_404


app_endpoint = "api/text_store"
search_endpoint = "api/search_service"
test_headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_single_text(http_service):
    test_endpoint = "text"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {
        "text_type": "transcript",
        "text_content": "<b>Hello</b> is it me you're looking for.",
        "text_format": "text/plain",
        "source_language": "spanish",
        "target_language": "english",
        "label": {
                "en": ["spanish transcription"],
                "es": ["transcripción en español"],
            },
    }
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    assert result.status_code == 201


def test_simple_fulltext_query(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "hello"}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    resp = result.json()
    assert result.status_code == requests.codes.ok
    assert resp["pagination"]["totalResults"] == 1
    assert resp["results"][0]["label"]["en"] == ['spanish transcription']
