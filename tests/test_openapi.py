from textwrap import dedent
from sticker.openapi import OpenAPISpec


def test_reading_paths():
    spec_text = dedent("""
    openapi: 3.0.0
    paths:
      /:
        get:
          operationId: dummy_handler
    """)

    spec = OpenAPISpec(spec_text)
    assert len(spec.paths()) == 1

    path = spec.paths()[0]
    assert path.url_path() == '/'
    assert len(path.operations()) == 1

    operation = path.operations()[0]
    assert operation.function_fullpath() == 'dummy_handler'
    assert operation.http_method() == 'GET'
