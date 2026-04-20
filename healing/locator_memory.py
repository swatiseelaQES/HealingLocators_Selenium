import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class LocatorMemory:
    def __init__(self, memory_path="results/locator_memory.json"):
        self.memory_path = memory_path
        self.store = self._load()

    def _load(self) -> Dict[str, List[dict]]:
        if not os.path.exists(self.memory_path):
            return {}
        with open(self.memory_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.store, f, indent=2)

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    @staticmethod
    def _locator_to_key(locator: Tuple[str, str]) -> dict:
        by, value = locator
        return {"by": by, "value": value}

    @staticmethod
    def _key_to_locator(entry: dict) -> Tuple[str, str]:
        return entry["by"], entry["value"]

    def get_locators(self, element_name: str) -> List[Tuple[str, str]]:
        entries = self.store.get(element_name, [])
        ranked = sorted(
            entries,
            key=lambda x: (x.get("success_count", 0), x.get("last_used", "")),
            reverse=True,
        )
        return [self._key_to_locator(entry) for entry in ranked]

    def remember(self, element_name: str, locator: Tuple[str, str], source="memory") -> None:
        entry = self._locator_to_key(locator)
        existing = self.store.setdefault(element_name, [])

        for item in existing:
            if item["by"] == entry["by"] and item["value"] == entry["value"]:
                item["success_count"] = item.get("success_count", 0) + 1
                item["last_used"] = self._now()

                # 🔥 PROMOTION LOGIC
                if item["success_count"] >= 2:
                    item["source"] = "memory"
                else:
                    item["source"] = source

                self._save()
                return

        # New entry
        existing.append({
            "by": entry["by"],
            "value": entry["value"],
            "success_count": 1,
            "last_used": self._now(),
            "source": source,
        })

        self._save()