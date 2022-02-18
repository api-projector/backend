def assert_paths(scheme: dict, paths: list[dict]):  # type: ignore
    """Asserts paths."""
    scheme_paths = []
    for scheme_url, scheme_path in scheme["paths"].items():
        for scheme_method, scheme_data in scheme_path.items():
            scheme_paths.append(
                {
                    "url": scheme_url[1:],
                    "method": scheme_method,
                    "json": scheme_data,
                },
            )

    assert scheme_paths == paths


def assert_schemas(scheme: dict, schemas: list[dict]):  # type: ignore
    """Asserts schemas."""
    scheme_schemas = []
    for scheme_name, scheme_data in scheme["components"]["schemas"].items():
        scheme_schemas.append(
            {
                "name": scheme_name,
                "json": scheme_data,
            },
        )

    assert scheme_schemas == schemas
