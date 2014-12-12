from nose.tools import assert_equal
from tui.protocol import generate_checktextformatrequest, \
                         parse_checktextformatrequest, \
                         generate_checktextformatresponse, \
                         parse_checktextformatresponse, \
                         generate_getscreeninforequest, \
                         parse_getscreeninforequest, \
                         generate_getscreeninforesponse, \
                         parse_getscreeninforesponse, \
                         generate_initsessionrequest, \
                         parse_initsessionrequest, \
                         generate_initsessionresponse, \
                         parse_initsessionresponse, \
                         generate_closesessionrequest, \
                         parse_closesessionrequest, \
                         generate_closesessionresponse, \
                         parse_closesessionresponse, \
                         generate_displayscreenrequest, \
                         parse_displayscreenrequest, \
                         generate_displayscreenresponse, \
                         parse_displayscreenresponse


def test_checktextformatrequest():
    text = 'AAAFVTGERGERFGREGREJGIERJGIERJGJEROIJJEIOJGOIJERIOGJEROIGJ'

    assert_equal(text,
                 parse_checktextformatrequest(generate_checktextformatrequest(text)))


def test_checktextformatresponse():
    ret = 0
    width = 300
    height = 25
    last_index = 63

    assert_equal((ret, width, height, last_index),
                 parse_checktextformatresponse(
                     generate_checktextformatresponse(ret, width, height, last_index)))


def test_getscreeninforequest():
    orientation = 1
    nbentryfields = 5

    assert_equal((orientation, nbentryfields),
                 parse_getscreeninforequest(
                     generate_getscreeninforequest(orientation, nbentryfields)))


def test_getscreeninforesponse():
    params = (0,
              8,
              8,
              8,
              8,
              2,
              3,
              5,
              (255, 128, 0),
              200,
              70,
              (
                  ('OK', 100, 25, True, True),
                  ('Cancel', 100, 1000, True, False),
                  ('Next', 300, 220, False, True),
                  ('Prev', 20, 25, True, False),
                  ('Back', 80, 250, False, False),
                  ('Forward', 90, 25, False, True)
              )
             )

    assert_equal(params,
                 parse_getscreeninforesponse(generate_getscreeninforesponse(*params)))


def test_initsessionrequest():
    parse_initsessionrequest(generate_initsessionrequest())


def test_initsessionresponse():
    ret = 0
    assert_equal(ret,
                 parse_initsessionresponse(generate_initsessionresponse(ret)))


def test_closesessionrequest():
    parse_closesessionrequest(generate_closesessionrequest())


def test_closesessionresponse():
    ret = 0
    assert_equal(ret,
                 parse_closesessionresponse(generate_closesessionresponse(ret)))


def test_displayscreenrequest():
    orientation = 1
    labelimage = ('PNGDATAxcvlksdlkjsdlfjslkjf', 320, 200)
    btnimage = ('PNGDATAxcvlksdlkjsdlfjslkjf', 320, 200)
    emptyimage = ('', 0, 0)
    label = ('LABEL TEXT', 5, 5, (128, 255, 128), labelimage, 0, 0)
    buttons = (
                  ('OK', emptyimage),
                  ('Cancel', emptyimage),
                  ('Next', emptyimage),
                  ('Prev', emptyimage),
                  ('Back', btnimage),
                  ('FWD', emptyimage),
    )
    requestedbuttons = (False, True, True, False, True, False)
    closetuisession = True
    entryfields = (
                      ('Your name', 1, 2, 3, 4),
                      ('Password', 2, 3, 4, 5)
    )

    params = (orientation,
              label,
              buttons,
              requestedbuttons,
              closetuisession,
              entryfields)

    assert_equal(params,
                 parse_displayscreenrequest(
                     generate_displayscreenrequest(*params)))


def test_displayscreenresponse():
    ret = 0
    button = 2
    entryfields = ('aaAAadjjidjqjiwjfioewjiofjewoifjweoifjewiofejwoifejwioefw',
                   'djqiwjdiqwodjicjwun23',
                   '420')

    params = (ret, button, entryfields)

    assert_equal(params,
                 parse_displayscreenresponse(
                     generate_displayscreenresponse(*params)))


