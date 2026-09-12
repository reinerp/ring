"""Check unwind control uses RIP, without executing native code."""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
source = (root / "crypto/fipsmodule/sha/asm/sha512-x86_64.pl").read_text()
handler = source.split("se_handler:\n", 1)[1].split(".Lin_prologue:", 1)[0]
after_restore = handler.split("mov\t%rbx,144($context)", 1)[1]
assert "mov\t248($context),%rbx" in after_restore.split("cmp\t%r10,%rbx", 1)[0]
print("SHA unwind dispatch reloads the interrupted instruction pointer.")
