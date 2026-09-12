"""Check unwind metadata without executing native code."""
from pathlib import Path
import sys

source = (Path(sys.argv[1]) / "crypto/cipher/asm/chacha20_poly1305_armv8.pl").read_text()
for name in ("seal", "open"):
    body = source.split(f"chacha20_poly1305_{name}:\n", 1)[1].split(f".L{name}_128:\n", 1)
    body = body[0] + body[1].split("\n", 1)[0]
    assert body.index(".cfi_remember_state") < body.index(".cfi_restore b15")
    assert body.index(".cfi_def_cfa_offset 0") < body.index(".cfi_restore_state")
print("Small-input bodies retain their active-frame unwind state.")
