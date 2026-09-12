"""Check native dispatch uses atomic getters without executing native code."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
reads = "\n".join((root / p).read_text() for p in
    ("crypto/fipsmodule/ec/p256-nistz.c", "crypto/fipsmodule/bn/internal.h"))
assert not re.search(r"\b(?:adx_bmi2|avx2|neon)_available\b", reads)
assert [reads.count(f"{f}_available_get()") for f in ("adx_bmi2", "avx2", "neon")] == [7, 2, 1]
print("All 10 native CPU feature reads use atomic getters.")
selection = (root / "build.rs").read_text().split("let generated_dir = if ", 1)[1].split(" {", 1)[0]
assert selection == "!is_git && c_root_dir.join(PREGENERATED).is_dir()"
print("Vendored Git builds regenerate missing assembly sources.")
