import io
import base64
import qrcode

def gen_qr_code(data):
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

save_qr_code()
