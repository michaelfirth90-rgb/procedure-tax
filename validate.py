import sys, glob
from html.parser import HTMLParser
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
class V(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.errs=[]
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        if tag == "p" and self.stack and self.stack[-1][0] == "p":
            self.errs.append((self.getpos(), f"<p> auto-closes previous <p> opened at line {self.stack[-1][1][0]}"))
            self.stack.pop()
        self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs): pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errs.append((self.getpos(), f"stray </{tag}>")); return
        if self.stack[-1][0] == tag:
            self.stack.pop(); return
        # find nearest matching
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                for t, p in self.stack[i+1:]:
                    self.errs.append((p, f"<{t}> never closed (closed by </{tag}> at line {self.getpos()[0]})"))
                del self.stack[i:]
                return
        self.errs.append((self.getpos(), f"stray </{tag}>"))

def check(path):
    v = V(); v.feed(open(path, encoding="utf-8").read())
    for t, p in v.stack:
        v.errs.append((p, f"<{t}> never closed"))
    return v.errs

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob("*.html"))
    total = 0
    for f in files:
        e = check(f)
        if e:
            total += 1
            print(f"\n{f}  ({len(e)} issue(s))")
            for pos, msg in e[:8]:
                print(f"   line {pos[0]:5} col {pos[1]:4}  {msg}")
    print(f"\n{total} of {len(files)} files with issues")
