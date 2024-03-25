import re


class RegexScanner:

    def __init__(self, pattern, text):
        self._requests = []
        self._text = text
        self._pattern = re.compile(pattern, re.IGNORECASE | re.DOTALL)
        self.scan()

    @property
    def requests(self):
        return self._requests

    def scan(self):
        matches = self._pattern.finditer(self._text)
        for match in matches:
            request = match.groupdict()
            self._requests.append(request)

    def attr_scan(self, attr):
        attrs = []
        for request in self._requests:
            attrs.append(request.get(attr, ""))
        return set(list(attrs))


if __name__ == "__main__":
    text = """[[Mediastinitis]], [[sepsis]]<ref name=Og2015/><ref name=Bau2020/>"""
    scanner = RegexScanner(
        r"<ref\s*name\s*=\s*[\"\']*(?P<name>[^>]*)[\"\']*\s*\/\s*>", text)
    for m in scanner.requests:
        print(m)
