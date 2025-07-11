import os
from typing import Any

import polib

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class BuildTranslationFiles(BuildHookInterface):

    SRC_DIR = os.path.join(os.path.dirname(__file__), "src")

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        for root, dirs, files in os.walk(BuildTranslationFiles.SRC_DIR):
            for file in files:
                if not file.endswith(".po"):
                    continue
                po_file = os.path.join(root, file)
                po = polib.pofile(po_file, check_for_duplicates=True)
                po.save_as_mofile(os.path.join(root, file.replace(".po", ".mo")))

    def clean(self, versions: list[str]) -> None:
        for root, dirs, files in os.walk(BuildTranslationFiles.SRC_DIR):
            for file in files:
                if not file.endswith(".mo"):
                    continue
                mo_file = os.path.join(root, file)
                os.remove(mo_file)