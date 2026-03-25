from bedrock_bio.list_datasets import list_datasets


class TestListDatasets:
    def test_returns_list_of_strings(self):
        result = list_datasets()
        assert isinstance(result, list)
        for name in result:
            assert isinstance(name, str)
