#!/usr/bin/env python3
"""Generate ASCII art text."""

import argparse
import sys


def block_style(text):
    """Block letter style."""
    return f"""
 █▀▀▀█ █   █ █▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀▀ █▀▀█
 █▄▄▄█ █   █ █▄▄█ █  █ █  █ █  █ █▀▀▀ █▄▄▀
 █  ▀  ▀▀▀▀▀ ▀  ▀ █▀▀▀ █▀▀▀ █  █ █▄▄▄ █ ▀ █"""


def shadow_style(text):
    """Shadow text style."""
    lines = []
    for char in text[:10]:  # Limit length
        if char == ' ':
            lines.append('   ')
        else:
            lines.append(f' [{char}]')
    return ''.join(lines)


def banner_style(text):
    """Banner style with borders."""
    width = len(text) + 4
    top = "╔" + "═" * (width - 2) + "╗"
    mid = "║ " + text + " ║"
    bot = "╚" + "═" * (width - 2) + "╝"
    return f"{top}\n{mid}\n{bot}"


def simple_block(text):
    """Simple block letters using basic chars."""
    result = []
    for char in text.upper():
        if char == 'A':
            result.append("  A  \n A A \nAAAAA\nA   A\nA   A")
        elif char == 'B':
            result.append("BBBB \nB   B\nBBBB \nB   B\nBBBB ")
        elif char == 'C':
            result.append(" CCC \nC    \nC    \nC    \n CCC ")
        elif char == 'D':
            result.append("DDDD \nD   D\nD   D\nD   D\nDDDD ")
        elif char == 'E':
            result.append("EEEEE\nE    \nEEE  \nE    \nEEEEE")
        elif char == 'F':
            result.append("FFFFF\nE    \nFFF  \nE    \nE    ")
        elif char == 'G':
            result.append(" GGG \nG    \nG  GG\nG   G\n GGG ")
        elif char == 'H':
            result.append("H   H\nH   H\nHHHHH\nH   H\nH   H")
        elif char == 'I':
            result.append("IIIII\n  I  \n  I  \n  I  \nIIIII")
        elif char == 'J':
            result.append("JJJJJ\n   J \n   J \nJ  J \n JJ  ")
        elif char == 'K':
            result.append("K  K \nK K  \nKK   \nK K  \nK  K ")
        elif char == 'L':
            result.append("L    \nL    \nL    \nL    \nLLLLL")
        elif char == 'M':
            result.append("M   M\nMM MM\nM M M\nM   M\nM   M")
        elif char == 'N':
            result.append("N   N\nNN  N\nN N N\nN  NN\nN   N")
        elif char == 'O':
            result.append(" OOO \nO   O\nO   O\nO   O\n OOO ")
        elif char == 'P':
            result.append("PPPP \nP   P\nPPPP \nP    \nP    ")
        elif char == 'Q':
            result.append(" QQQ \nQ   Q\nQ Q Q\nQQ  \n QQQQ")
        elif char == 'R':
            result.append("RRRR \nR   R\nRRRR \nR R  \nR  RR")
        elif char == 'S':
            result.append(" SSS \nS    \n SSS \n    S\nSSSS ")
        elif char == 'T':
            result.append("TTTTT\n  T  \n  T  \n  T  \n  T  ")
        elif char == 'U':
            result.append("U   U\nU   U\nU   U\nU   U\n UUU ")
        elif char == 'V':
            result.append("V   V\nV   V\n V V \n V V \n  V  ")
        elif char == 'W':
            result.append("W   W\nW   W\nW W W\nWW WW\nW   W")
        elif char == 'X':
            result.append("X   X\n X X \n  X  \n X X \nX   X")
        elif char == 'Y':
            result.append("Y   Y\n Y Y \n  Y  \n  Y  \n  Y  ")
        elif char == 'Z':
            result.append("ZZZZZ\n   Z \n  Z  \n Z   \nZZZZZ")
        elif char == ' ':
            result.append("     \n     \n     \n     \n     ")
        else:
            result.append(f" [{char}] ")
    
    # Combine horizontally (max 5 chars per line for readability)
    combined = []
    for i in range(0, len(result), 5):
        chunk = result[i:i+5]
        for row in range(5):
            line = "  ".join(letter.split('\n')[row] for letter in chunk)
            combined.append(line)
    
    return '\n'.join(combined)


def main():
    parser = argparse.ArgumentParser(description="Generate ASCII art")
    parser.add_argument("--text", "-t", required=True, help="Text to convert")
    parser.add_argument("--style", "-s", default="banner",
                       choices=["block", "shadow", "banner", "simple"],
                       help="ASCII art style")
    parser.add_argument("--output", "-o", help="Output file (optional, prints to stdout)")
    
    args = parser.parse_args()
    
    styles = {
        "block": block_style,
        "shadow": shadow_style,
        "banner": banner_style,
        "simple": simple_block,
    }
    
    generator = styles.get(args.style)
    if generator:
        result = generator(args.text)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"✅ ASCII art saved to: {args.output}")
        else:
            print(result)
    else:
        print(f"❌ Unknown style: {args.style}")
        sys.exit(1)


if __name__ == "__main__":
    main()
