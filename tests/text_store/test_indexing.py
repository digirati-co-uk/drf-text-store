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
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert response_json["results"][0]["label"]["en"] == ['spanish transcription']


def test_transcript(http_service):
    test_endpoint = "text"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {
        "text_type": "translation",
        "text_content": "<p>the one with the wind jewel, the one with the turkey blood design, or the one with the"
            " whirlpool design, the one with the smoking mirror. </p>\n<p>All these various things they "
            "presented to [the Spaniards. These] gave them gifts in return. They offered them green and"
            " yellow necklaces which resembled amber.[^5] </p>\n<p>And when they had taken [the gift], "
            "when they had seen it, much did they marvel. </p>\n<p>And [the Spaniards] addressed them; "
            'they said to them: "Go! For the time being we depart for Castile. We shall not tarry in '
            'going to reach Mexico." </p>\n<p>Thereupon [the Spaniards] went. Thereupon also [the others]'
            " came back; they turned back. </p>\n<p>And when they had come to emerge on dry land, then"
            " they went direct to Mexico. Day by day, night by "
            'night<a href="_Ibid_.:" title="_en vn dia, y en vna noche_.">^6</a> they traveled in '
            "order to come to warn Moctezuma, in order to come to tell him exactly of its "
            "circumstances; they came to notify him.[^7] Their goods had come to be what they had gone"
            ' to receive. </p>\n<p>And thereupon they addressed him: "O our lord, O my noble youth, '
            "may thou destroy us. For behold what we have seen, behold what we have done, there where"
            "thy grandfathers stand guard for thee before the ocean. For we went to see our lords the"
            " gods in the midst of the water. All thy capes we went to give them. And behold their "
            "noble goods which they gave us.</p>\n"
            '<p>[^5]: Spanish text: "<em>los españoles dieron a los indios cuētas de vidrio, '
            'vnas verdes y otras amarillas</em>."</p>\n<p>[^7]: Seler, <em>Einige Kapitel</em>, '
            'p. 458, has <em>ivel ioca</em>, translated "first of all." '
            "Garibay (Sahagún, Garibay ed., Vol. IV, p. 84) translates "
            'the passage thus: "<em>Día y noche vinieron caminando para comunicar a '
            'Motecuzoma, para decirle y darle a saber con verdad lo que él pudiera saber</em>." </p>',
        "text_format": "text/plain",
        "source_language": "nci",
        "target_language": "en",
        "label": {
                "en": ["nahuatl translation"],
                "es": ["traducción al náhuatl"],
            },
    }
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    assert result.status_code == 201


def test_translation_query(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "turkey blood"}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert response_json["results"][0]["label"]["es"] == ["traducción al náhuatl"]
    assert "<b>turkey</b> <b>blood</b>" in response_json["results"][0].get(
        "snippet", None
    )


def test_translation_query_with_facet(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "mirror",
                 "facets": [{"type": "text", "subtype": "label", "value": "traducción al náhuatl",
                             "language_display": "spanish"}]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert "<b>mirror</b>" in response_json["results"][0].get(
        "snippet", None
    )


def test_translation_query_with_facet_fail(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "mirror",
                 "facets": [{"type": "text", "subtype": "label", "value": "rhubarb",
                             "language_display": "english"}]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 0


def test_translation_query_with_text_fail(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "rhubarb",
                 "facets": [{"type": "text", "subtype": "label", "value": "traducción al náhuatl",
                             "language_display": "spanish"}]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 0


def test_translation_query_with_facet_different_language(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "mirror",
                 "facets": [{"type": "text", "subtype": "label", "value": "nahuatl translation",
                             "language_display": "english"}]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert "<b>mirror</b>" in response_json["results"][0].get(
        "snippet", None
    )


def test_translation_query_with_resource_filter(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "mirror",
                 "resource_filters": [
                    {
                        "value": "text/plain",
                        "field": "text_format",
                        "operator": "exact",
                        "resource_class": "textresource",
                    }]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert "<b>mirror</b>" in response_json["results"][0].get(
        "snippet", None
    )


def test_translation_query_with_resource_filter_fail(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "mirror",
                 "resource_filters": [
                    {
                        "value": "application/json+ld",
                        "field": "text_format",
                        "operator": "exact",
                        "resource_class": "textresource",
                    }]}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 0


def test_text_resource_blank_fields(http_service):
    test_endpoint = "text"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {
        "text_type": "transcript",
        "text_content": "El facóquero común o facocero común",
        "text_format": "text/plain",
        "source_language": "spanish",
        "target_language": "english",
        "text_title": "  ",
        "text_subtitle": "  ",
        "label": {
                "en": ["Common warthog"],
                "es": ["El facóquero común"],
            },
    }
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    assert result.status_code == 201


def test_text_resource_blank_fields_indexing(http_service):
    test_endpoint = "text_search"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    post_json = {"fulltext": "facocero"}
    result = requests.post(
        url=f"{http_service}/{app_endpoint}/{test_endpoint}",
        json=post_json,
        headers=headers,
    )
    response_json = result.json()
    assert result.status_code == requests.codes.ok
    assert response_json["pagination"]["totalResults"] == 1
    assert response_json["results"][0]["label"]["en"] == ['Common warthog']


