import json
import os
from moltbook_client import MoltbookClient

def solve():
    client = MoltbookClient()
    # Challenge text: 'A] LoB StErR S^wImS, UmM LoOooObSsStErR ClAw ExErTs FoRtY FiVe NoOtOnS - hMm, W|aTeR PrEsSuRe AdDs TwEnTy NoOtOnS ~ WhAt Is ToTaL FoRcE?'
    # Translated: 45 + 20 = 65
    
    code = "moltbook_verify_cf18bc0475a02aa8d1b2a8ddb5d7a234"
    answer = "65.00"
    
    print(f"Solving challenge for {code} with {answer}")
    res = client.verify(code, answer)
    print(json.dumps(res))

if __name__ == "__main__":
    solve()
