"""Check counter wrapping by source inspection, without executing crypto."""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
source = (root / "src/aead/chacha/fallback.rs").read_text()
assert "state[12] = state[12].wrapping_add(1);" in source
assert "state[12] += 1;" not in source
print("Fallback counter increment wraps independently of overflow-check settings.")
