# HTMLSmuggler
This tool embeds a file into a standalone HTML that automatically triggers a download when opened in a browser. To customize the generated HTML, edit the template inside `htmlsmuggler.py`. For research and educational use only.

## Usage:
```
python3 htmlsmuggler.py -f input.exe -o output.html
```
```
python3 htmlsmuggler.py -f input.exe -o output.html --xor
```
## MITRE ATT&CK mapping:
T1027.006 - Obfuscated Files or Information: HTML Smuggling

