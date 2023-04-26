from opensearchpy import OpenSearch

index_name = "turism_routes_madrid"

if not OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "admin"),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
).indices.exists(index=index_name):
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "admin"),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "object": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "details": {"type": "object", "enabled": True},
            }
        }
    }

    client.indices.create(index=index_name, body=mapping)
    print(f"Index {index_name} created successfully!")
    client.close()

else:
    print(f"Index {index_name} already exists. Nothing to do.")
