import qrcode

qr = qrcode.QRCode()
qr.add_data("https://example.com")
qr.make(fit=True)
img = qr.make_image()
img.save("test.png")
print("generate QR code successful")
