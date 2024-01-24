from typing import Any, Dict, List, Optional

from engine.base_client import IncompatibilityError
from engine.base_client.parser import BaseConditionParser, FieldValue


class ChromaConditionParser(BaseConditionParser):
    def parse(self, meta_conditions: Dict[str, Any]) -> Optional[Any]:
        if meta_conditions is None or len(meta_conditions) == 0:
            return None
        return super().parse(meta_conditions)

    def build_condition(
            self, and_subfilters: Optional[List[Any]], or_subfilters: Optional[List[Any]]
    ) -> Optional[Any]:
        clause = {}
        use_or_filter = or_subfilters is not None and len(or_subfilters) > 0
        use_and_filter = and_subfilters is not None and len(and_subfilters) > 0

        if use_or_filter and use_and_filter:
            raise IncompatibilityError("Both 'and' and 'or' filters are not supported by the benchmark.")

        if use_or_filter:
            if len(or_subfilters) == 1:
                clause = or_subfilters[0]
            else:
                clause = {
                    "$or": or_subfilters,
                }
        if use_and_filter:
            if len(and_subfilters) == 1:
                clause = and_subfilters[0]
            else:
                clause = {
                    "$and": and_subfilters,
                }
        return clause

    def build_exact_match_filter(self, field_name: str, value: FieldValue) -> Any:
        return {
            field_name: value
        }
