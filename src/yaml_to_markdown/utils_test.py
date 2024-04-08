from yaml_to_markdown.utils import convert_to_title_case


class TestUtils:
    def test_convert_to_title_case(self) -> None:
        assert convert_to_title_case("test-case") == "Test Case"
