import contextlib
import unittest

from cloudinary.utils import normalize_expression, generate_transformation_string

NORMALIZATION_EXAMPLES = {
    'None is not affected': [None, None],
    'number replaced with a string value': [10, '10'],
    'empty string is not affected': ['', ''],
    'single space is replaced with a single underscore': [' ', '_'],
    'blank string is replaced with a single underscore': ['   ', '_'],
    'underscore is not affected': ['_', '_'],
    'sequence of underscores and spaces is replaced with a single underscore': [' _ __  _', '_'],
    'arbitrary text is not affected': ['foobar', 'foobar'],
    'double ampersand replaced with and operator': ['foo && bar', 'foo_and_bar'],
    'double ampersand with no space at the end is not affected': ['foo&&bar', 'foo&&bar'],
    'width recognized as variable and replaced with w': ['width', 'w'],
    'initial aspect ratio recognized as variable and replaced with iar': ['initial_aspect_ratio', 'iar'],
    'duration is recognized as a variable and replaced with du': ['duration', 'du'],
    'duration after : is not a variable and is not affected': ['preview:duration_2', 'preview:duration_2'],
    '$width recognized as user variable and not affected': ['$width', '$width'],
    '$initial_aspect_ratio recognized as user variable followed by aspect_ratio variable': [
        '$initial_aspect_ratio',
        '$initial_ar',
    ],
    '$mywidth recognized as user variable and not affected': ['$mywidth', '$mywidth'],
    '$widthwidth recognized as user variable and not affected': ['$widthwidth', '$widthwidth'],
    '$_width recognized as user variable and not affected': ['$_width', '$_width'],
    '$__width recognized as user variable and not affected': ['$__width', '$_width'],
    '$$width recognized as user variable and not affected': ['$$width', '$$width'],
    '$height recognized as user variable and not affected': ['$height_100', '$height_100'],
    '$heightt_100 recognized as user variable and not affected': ['$heightt_100', '$heightt_100'],
    '$$height_100 recognized as user variable and not affected': ['$$height_100', '$$height_100'],
    '$heightmy_100 recognized as user variable and not affected': ['$heightmy_100', '$heightmy_100'],
    '$myheight_100 recognized as user variable and not affected': ['$myheight_100', '$myheight_100'],
    '$heightheight_100 recognized as user variable and not affected': [
        '$heightheight_100',
        '$heightheight_100',
    ],
    '$theheight_100 recognized as user variable and not affected': ['$theheight_100', '$theheight_100'],
    '$__height_100 recognized as user variable and not affected': ['$__height_100', '$_height_100']
}


class ExpressionNormalizationTest(unittest.TestCase):
    def test_expression_normalization(self):
        for description, (input_expression, expected_expression) in NORMALIZATION_EXAMPLES.items():
            with self.subTest(description, input_expression=input_expression):
                self.assertEqual(expected_expression, normalize_expression(input_expression))

    if not hasattr(unittest.TestCase, "subTest"):
        # Support Python before version 3.4
        @contextlib.contextmanager
        def subTest(self, msg="", **params):
            yield
