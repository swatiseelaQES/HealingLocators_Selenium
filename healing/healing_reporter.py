import json
import os
from datetime import datetime


class HealingReporter:
    def __init__(self, report_path="results/healing_report.json"):
        self.report_path = report_path
        self.events = []

    def record_success(
        self,
        element_name,
        locator,
        healed=False,
        fallback_locator=None,
        screenshot=None,
        heal_source=None,
    ):
        self.events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "element_name": element_name,
            "status": "healed" if healed else "primary_success",
            "heal_source": heal_source,
            "primary_locator": str(locator),
            "fallback_locator": str(fallback_locator) if fallback_locator else None,
            "screenshot": screenshot,
        })

    def record_failure(self, element_name, locator, fallback_locators):
        self.events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "element_name": element_name,
            "status": "failed",
            "heal_source": None,
            "primary_locator": str(locator),
            "fallback_locators": [str(x) for x in fallback_locators],
            "screenshot": None,
        })

    def write_report(self):
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        with open(self.report_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": {
                        "total_events": len(self.events),
                        "healed_count": len([e for e in self.events if e["status"] == "healed"]),
                        "primary_success_count": len([e for e in self.events if e["status"] == "primary_success"]),
                        "failed_count": len([e for e in self.events if e["status"] == "failed"]),
                        "memory_healed_count": len(
                            [e for e in self.events if e["status"] == "healed" and e["heal_source"] == "memory"]
                        ),
                        "fallback_healed_count": len(
                            [e for e in self.events if e["status"] == "healed" and e["heal_source"] == "fallback"]
                        ),
                    },
                    "events": self.events,
                },
                f,
                indent=2,
            )