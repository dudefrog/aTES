import json
from pathlib import Path
from typing import Optional

import jsonschema
from pydantic import BaseModel

SCHEMAS_PATH = Path(__file__).parent.parent / "schemas"


class ValidationResult(BaseModel):
    ok: bool
    error: Optional[jsonschema.ValidationError] = None

    class Config:
        arbitrary_types_allowed = True


class Schema:
    def __init__(self, event_name: str):
        self.event = event_name

        parts = event_name.split(".")
        parts[-1] += ".json"
        self.schema_path = SCHEMAS_PATH.joinpath("/".join(parts))
        if not (self.schema_path.exists()):
            raise ValueError(
                f"Schema for {event_name} does not exist at {self.schema_path}"
            )

    def validate(self, data: dict):
        schema = json.loads(self.schema_path.read_text())
        jsonschema.validate(instance=data, schema=schema)
