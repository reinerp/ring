"""Check saved-frame slot correspondence without executing native code."""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
source = (root / "crypto/fipsmodule/bn/asm/x86_64-mont5.pl").read_text()
handler = source.split("mul_handler:\n", 1)[1].split(".Lcommon_pop_regs:", 1)[0]
assert "8(%rax,%r10,8)" not in handler
assert "mov\t40(%rax),%rax" in handler
print("Retained Montgomery bodies unwind using the fixed saved-RSP slot.")
