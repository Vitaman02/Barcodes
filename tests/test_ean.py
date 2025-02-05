import pytest
from PIL import Image

from pybarcodes import EAN8, EAN13, EAN14, JAN
from pybarcodes.exceptions import IncorrectFormat


def test_ean13(fs):
    code = "400638133393"
    barcode = EAN13(code)
    barcode2 = EAN13(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    assert barcode == code + "1"
    assert barcode == barcode2

    # Check image
    image = barcode.image

    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    assert image.size == tuple(
        map(sum, zip(barcode.BARCODE_SIZE, barcode.BARCODE_PADDING))
    )

    # Save image to fake file
    file = fs.create_file("barcode.png")
    barcode.save(file.path, size=(100, 100))
    assert file.byte_contents[:8] == b"\x89PNG\r\n\x1a\n"

    # Check if the checksum digit is calculated correctly
    # The check digit should be `1`
    code = "400638133393"
    checkdigit = EAN13.calculate_checksum(code)
    assert checkdigit == 1

    code = "40063813339398736412039867123409586345"
    barcode = EAN13(code)
    # The check digit is calculated when instansiating
    assert barcode == "4006381333931"

    with pytest.raises(IncorrectFormat):
        code = "1"
        barcode = EAN13(code)

    # Check if guards are in the correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_ean8(fs):
    code = "0123456"
    barcode = EAN8(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert not barcode.HAS_STRUCTURE

    # Check image
    image = barcode.image

    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    assert image.size == tuple(
        map(sum, zip(barcode.BARCODE_SIZE, barcode.BARCODE_PADDING))
    )

    # Save image to fake file
    file = fs.create_file("barcode.png")
    barcode.save(file.path, size=(100, 100))
    assert file.byte_contents[:8] == b"\x89PNG\r\n\x1a\n"

    # Check digit for this barcode should be `5`
    assert EAN8.calculate_checksum(code) == 5

    code = "012345628743652398476528347652987"
    barcode = EAN8(code)

    # The check digit is calculated when instantiating
    assert barcode == "01234565"

    with pytest.raises(IncorrectFormat):
        code = "1"
        barcode = EAN8(code)

    # Check if guards in correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[33:38]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_ean14(fs):
    code = "4070071967072013242346"
    barcode = EAN14(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    # Check image
    image = barcode.image

    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    assert image.size == tuple(
        map(sum, zip(barcode.BARCODE_SIZE, barcode.BARCODE_PADDING))
    )

    # Save image to fake file
    file = fs.create_file("barcode.png")
    barcode.save(file.path, size=(100, 100))
    assert file.byte_contents[:8] == b"\x89PNG\r\n\x1a\n"

    # Check digit for this barcode should be `0`
    assert EAN14.calculate_checksum(code) == 0

    # The check digit is calculated when instantiating
    assert barcode == "40700719670720"

    with pytest.raises(IncorrectFormat):
        code = "1"
        barcode = EAN14(code)

    # Check if guards in correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"


def test_jan(fs):
    code = "450638133393"
    barcode = JAN(code)
    barcode2 = JAN(code)

    # Check if the required attributes exist
    assert barcode.BARCODE_LENGTH
    assert barcode.BARCODE_SIZE
    assert barcode.BARCODE_FONT_SIZE
    assert barcode.BARCODE_COLUMN_NUMBER
    assert barcode.BARCODE_PADDING
    assert barcode.FIRST_SECTION
    assert barcode.SECOND_SECTION
    assert barcode.WEIGHTS
    assert barcode.HAS_STRUCTURE

    assert barcode == code + "6"
    assert barcode == barcode2

    # Check image
    image = barcode.image

    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    assert image.size == tuple(
        map(sum, zip(barcode.BARCODE_SIZE, barcode.BARCODE_PADDING))
    )

    # Save image to fake file
    file = fs.create_file("barcode.png")
    barcode.save(file.path, size=(100, 100))
    assert file.byte_contents[:8] == b"\x89PNG\r\n\x1a\n"

    # Check if the checksum digit is calculated correctly
    # The check digit should be `1`
    code = "450638133393"
    checkdigit = JAN.calculate_checksum(code)
    assert checkdigit == 6

    code = "45063813339398736412039867123409586345"
    barcode = JAN(code)
    # The check digit is calculated when instansiating
    assert barcode == "4506381333936"

    with pytest.raises(IncorrectFormat):
        code = "1"
        barcode = JAN(code)

    # Check if guards are in the correct positions
    binary_string = barcode.get_binary_string
    left_guard = binary_string[:3]
    right_guard = binary_string[-3:]
    center_guard = binary_string[45:50]
    assert left_guard == "101"
    assert right_guard == "101"
    assert center_guard == "01010"
