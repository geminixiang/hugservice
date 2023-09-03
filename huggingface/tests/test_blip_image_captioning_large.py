from ..blip_image_captioning_large import blip_image_captioning_large


def test_blip_image_captioning_large():
    img_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg"
    text = blip_image_captioning_large(img_url)
    assert text.startswith("a photography of")