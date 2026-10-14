import subprocess

PRINTER = "STMicroelectronics_POS58_Printer_USB"  # from lpstat -p

ESC = b"\x1b"
GS = b"\x1d"
INIT = ESC + b"@"
CENTER = ESC + b"a\x01"
LEFT = ESC + b"a\x00"
BIG = GS + b"!\x33"      # 4x width and height
NORMAL = GS + b"!\x00"
BOLD_ON = ESC + b"E\x01"
BOLD_OFF = ESC + b"E\x00"
CODEPAGE_850 = b"\x1bt\x02"   # ESC t 2

def print_highscore(score, queue=PRINTER):
    data = (
        INIT
        + CODEPAGE_850
        + CENTER + BOLD_ON + b"BOUNCETRUCK\n" + BOLD_OFF
        + b"\n"
        + "Marché Noir 2026".encode("cp850")
        + b"\n\n"
        + BIG + str(int(score)).encode("ascii") + b"\n" + NORMAL
        + LEFT + b"\n\n\n\n"   # feed so the slip clears the tear bar
    )
    subprocess.Popen(
        ["/usr/bin/lpr", "-P", queue, "-o", "raw"],
        stdin=subprocess.PIPE,
    ).communicate(data)

print_highscore(1234)