from dataclasses import dataclass


@dataclass
class OperatorSource:
    """Operator's connection to the source and weight"""
    operator_id: int
    source_id: int
    weight: int
