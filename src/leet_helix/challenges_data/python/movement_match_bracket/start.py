def get_nested_value(x):
    pass

def get_records():
    data = [
        (
            "id_alpha",
            "This tuple contains (parentheses) to confuse simple searches",
            {"meta": (1, 2), "active": True}
        )
        [
            "id_beta",
            "This is a list block [with brackets]",
            get_nested_value(x=(10 + 5))
        ]
        {
            "id": "gamma",
            "type": "dict",
            "value": None
        }
    ]
    return data
