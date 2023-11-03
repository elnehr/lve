from lve.checkers.base import BaseChecker
from lve.utils.importutils import ensure_installed

class PII_Checker(BaseChecker):

    def __init__(self, entities: list[str]):
        super().__init__()
        ensure_installed("presidio_analyzer")
        from presidio_analyzer import AnalyzerEngine
        self.analyzer = AnalyzerEngine()
        self.entities = entities

    def is_safe(self, prompt, response, param_values) -> bool:
        results = self.analyzer.analyze(text=response, language='en')
        for res in results:
            if res.entity_type in self.entities:
                return False
        return True

    def postprocess_response(self, response):
        results = self.analyzer.analyze(text=response, language='en')
        mask_map = {}
        for res in results:
            if res.entity_type in self.entities:
                mask_map[response[res.start:res.end]] = f"<{res.entity_type}>"
                
        for sub, mask in mask_map.items():
            response = response.replace(sub, mask)
        return response

