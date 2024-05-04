import urllib.parse

def generate_qr(data: str, size: int = 350, margin: int = 25) -> str:
    """
    Calls QR Generator API to create a QR code storing the data passed
    :param data: string data to be encoded
    :param size: size of the QR code in pixels

    :return: URL to the QR code
    """
    encoded_data = urllib.parse.quote(data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin={margin}&data={encoded_data}"

