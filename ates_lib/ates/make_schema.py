from pathlib import Path
from string import Template
from textwrap import dedent

import typer

SCHEMAS_PATH = Path(__file__).parent.parent / "schemas"
SCHEMA_TEMPLATE = Template(
    """
{
"$$schema": "http://json-schema.org/draft-04/schema#",

"title": "$title",
"description": "json schema for $description event (version $version)",

"definitions": {
    "event_data": {
    "type": "object",
    "properties": {},
    "required": []
    }
},

"type": "object",

"properties": {
    "event_id": { "type": "string" },
    "event_version": { "enum": [$versions] },
    "event_name": { "type": "string" },
    "event_time": { "type": "string" },
    "producer": { "enum": ["auth", "billing", "task_tracker"] },

    "data": { "$$ref": "#/definitions/event_data" }
},

"required": [
    "event_id",
    "event_version",
    "event_name",
    "event_time",
    "producer",
    "data"
]
}
"""
)

app = typer.Typer()


@app.command()
def generate_event_schema(
    event: str = typer.Argument(..., help="Event name, e.g task.created")
):
    parts = event.split(".")
    evt_root_path = SCHEMAS_PATH.joinpath("/".join(parts))
    version = 1
    versions = "1"
    if evt_root_path.exists():
        existing_versions = sorted([p.stem for p in evt_root_path.glob("*.json")])
        if existing_versions:
            version = int(existing_versions[-1]) + 1
            versions = ", ".join(existing_versions + [str(version)])
    title = ".".join([p.capitalize() for p in parts]) + f".v{version}"

    body = SCHEMA_TEMPLATE.substitute(
        title=title,
        description=" ".join(parts),
        version=version,
        versions=versions,
    )

    evt_path = evt_root_path / f"{version}.json"
    evt_root_path.mkdir(parents=True, exist_ok=True)
    evt_path.write_text(body)
    print(f"{title} written")


def main():
    app()


if __name__ == "__main__":
    main()
