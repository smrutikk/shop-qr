import qrcode

shop_id = 1
url = f"https://shop-qr.onrender.com/print/{shop_id}"

img = qrcode.make(url)
img.save(f"shop_{shop_id}_qr.png")

print("QR generated for:", url)
