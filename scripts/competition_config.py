from itertools import product, chain

import yaml

sm = snakemake  # noqa

tasks = {
    phase: [
        {
            "index": len(sm.params.phases) * i + j,
            "name": f"{generator.upper()}(ε={epsilon})",
            "scoring_program": "scoring_program/",
            "reference_data": f"reference_data/{phase}/{generator}_{epsilon}/",
        }
        for i, (generator, epsilon) in enumerate(
            product(sm.params.tasks["generator"], sm.params.tasks["epsilon"])
        )
    ]
    for j, phase in enumerate(sm.params.phases)
}

solutions = [
    {
        "index": task["index"],
        "tasks": [task["index"]],
        "path": task["reference_data"]
    }
    for task in chain.from_iterable(tasks.values())
]

competition = {
    "version": 2,
    "title": "SNAKE #1",
    "description": "SaNitization Algorithms under attacK",
    "image": "logo.png",
    "terms": "pages/terms.md",
    "registration_auto_approve": True,
    "pages": [
        {"title": "Overview", "file": "pages/overview.md"},
        {"title": "Getting Started", "file": "pages/getting_started.md"},
        {"title": "Data", "file": "pages/data.md"},
        {"title": "Evaluation", "file": "pages/evaluation.md"},
        {"title": "Terms", "file": "pages/terms.md"},
    ],
    "phases": [
        {
            "name": phase["name"],
            "description": phase["description"],
            "start": phase["start"],
            "end": phase["end"],
            "max_submissions_per_day": sm.params.max_submissions_per_day,
            "max_submissions": sm.params.max_submissions,
            "tasks": [task["index"] for task in tasks[name]],
        }
        for name, phase in sm.params.phases.items()
    ],
    "tasks": list(chain.from_iterable(tasks.values())),
    "solutions": solutions,
    "leaderboards": [
        {
            "title": "Results",
            "key": "results",
            "columns": [
                {
                    "title": "Membership Advantage",
                    "key": "ma",
                    "index": 0,
                    "sorting": "desc",
                }
            ],
        }
    ],
    "fact_sheet": {
        "url": {
            "key": "url",
            "type": "text",
            "title": "URL",
            "selection": "",
            "is_required": False,
            "is_on_leaderboard": False
        }
    }
}

with open(sm.output[0], "w") as f:
    yaml.dump(competition, f, allow_unicode=True, sort_keys=False)
