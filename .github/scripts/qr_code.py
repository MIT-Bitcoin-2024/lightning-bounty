import io
import sys
import base64
import urllib.parse
# import qrcode

def gen_qr_code(data):
    """
    For use like this:
    f"![QR code](data:image/png;base64,{qr_code_data.decode('utf-8')})"
    but not supported in gh-flavored markdown
    """
    qr_pil = qrcode.make(data)
    buf = io.BytesIO()
    qr_pil.save(buf)
    qr_base64 = base64.b64encode(buf.getvalue())
    return qr_base64

# data = "lnbc20n1pnzgkh0pp5k2d7frgeqsmsgg3afl9x9m72s6kl5rpg22qhav4npwk3x98lc58sdqgdpjkcmr0cqzzsxqrrsssp53lyem2rze66e9ecml8hpx4ua34wengqhmpf905xrf5cp55cpak5q9qyyssqnllnx5kqam7ewekcg68cryhg6gdr2glaqvjl350txrajrp0rsqvshkehp5fffmxgza2z7j9044wrja329xs7mfe4k90cnxcyex4pc0spq7puf7"
# qr_code = gen_qr_code(data)
# print(qr_code.decode('utf-8'))

def save_qr_code():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data("https://example.com")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")

# save_qr_code()

def generate_qr(data: str, size: int = 250) -> str:
    """
    Calls QR Generator API to create a QR code storing the data passed
    :param data: string data to be encoded
    :param size: size of the QR code in pixels

    :return: URL to the QR code
    """
    encoded_data = urllib.parse.quote(data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded_data}"

# print(f'sys.argv: {sys.argv}')
data = "lnbc20n1pnzgkh0pp5k2d7frgeqsmsgg3afl9x9m72s6kl5rpg22qhav4npwk3x98lc58sdqgdpjkcmr0cqzzsxqrrsssp53lyem2rze66e9ecml8hpx4ua34wengqhmpf905xrf5cp55cpak5q9qyyssqnllnx5kqam7ewekcg68cryhg6gdr2glaqvjl350txrajrp0rsqvshkehp5fffmxgza2z7j9044wrja329xs7mfe4k90cnxcyex4pc0spq7puf7"
# generate_qr(data)
