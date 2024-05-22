import argparse
from PIL import Image, ImageFilter


def apply_effects(input_path, output_path):
    original_image = Image.open(input_path)
    resized_image = original_image.resize((348, 550))
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(20))
    blurred_image.save(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ur mom")
    parser.add_argument("input_path", help="image file path")
    parser.add_argument("output_path", help="output file path")
    args = parser.parse_args()

    apply_effects(args.input_path, args.output_path)
