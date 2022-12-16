from compas_rrc.parsers.abb import parser


def test_dec_integer():
    rapid_text = "312"
    ast = parser.parse(rapid_text)
    assert ast == 312


def test_hex_integer():
    rapid_text = "0xFFFFFFFF"
    ast = parser.parse(rapid_text)
    assert ast == 4294967295


def test_oct_integer():
    rapid_text = "0o377"
    ast = parser.parse(rapid_text)
    assert ast == 255


def test_bin_integer():
    rapid_text = "0b11111110"
    ast = parser.parse(rapid_text)
    assert ast == 254


def test_string():
    rapid_text = '"Hello RRC"'
    ast = parser.parse(rapid_text)
    assert ast == "Hello RRC"


def test_empty_string():
    rapid_text = '""'
    ast = parser.parse(rapid_text)
    assert ast == ""


def test_float():
    rapid_text = "-488.016"
    ast = parser.parse(rapid_text)
    assert ast == -488.016


def test_exponential():
    rapid_text = "2E2"
    ast = parser.parse(rapid_text)
    assert ast == 200


def test_bool():
    rapid_text = "FALSE"
    ast = parser.parse(rapid_text)
    assert ast is False

    rapid_text = "TRUE"
    ast = parser.parse(rapid_text)
    assert ast is True


def test_record():
    rapid_text = '[FALSE,TRUE,"Hi", 231, 2553.43]'
    ast = parser.parse(rapid_text)
    assert ast == [False, True, "Hi", 231, 2553.43]


def test_nested_record():
    rapid_text = '[[FALSE,TRUE],["Bye"], [231, 2553.43]]'
    ast = parser.parse(rapid_text)
    assert ast == [[False, True], ["Bye"], [231, 2553.43]]


def test_whitespace():
    rapid_text = '    [FALSE,        TRUE,      "Hi"]  '
    ast = parser.parse(rapid_text)
    assert ast == [False, True, "Hi"]
