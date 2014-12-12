from struct import pack, unpack, calcsize

class Error(Exception):
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return repr(self.value)


fmt_checktextformatrequest = 'I'
fmt_checktextformatresponse = 'IIII'

TUI_MSGTYPE_CHECKTEXTFORMATREQUEST = 0x01
TUI_MSGTYPE_CHECKTEXTFORMATRESPONSE = 0x02
TUI_MSGTYPE_GETSCREENINFOREQUEST = 0x03
TUI_MSGTYPE_GETSCREENINFORESPONSE = 0x04
TUI_MSGTYPE_INITSESSIONREQUEST = 0x05
TUI_MSGTYPE_INITSESSIONRESPONSE = 0x06
TUI_MSGTYPE_CLOSESESSIONREQUEST = 0x07
TUI_MSGTYPE_CLOSESESSIONRESPONSE = 0x08
TUI_MSGTYPE_DISPLAYSCREENREQEUST = 0x09
TUI_MSGTYPE_DISPLAYSCREENRESPONSE = 0x0A


def generate_lengthvalue(data):
    return pack('I', len(data)) + data


def parse_lengthvalue(msg):
    length = unpack('I', msg[0:4])[0]
    return length, msg[4:4+length]


def generate_message(msg_type, data):
    return pack('II', msg_type, len(data)) + data


def parse_message(message):
    # Parse message type and length from binary data
    msg_type, msg_len = unpack('II', message[0:8])
    data = message[8:]

    # Verify size of packet is valid
    if len(data) != msg_len:
        raise Error('Data length not same as given in message header')

    return (msg_type, data)


def parse_message_of_type(msg_type, message):
    parsed_msg_type, data = parse_message(message)

    if parsed_msg_type != msg_type:
        raise(Error('Invalid message type  parsed: %02x expected: %02x' %
                    (parsed_msg_type, msg_type)))

    return data


def generate_checktextformatrequest(text):
    return generate_message(TUI_MSGTYPE_CHECKTEXTFORMATREQUEST,
                            pack('I', len(text)) + text)


def parse_checktextformatrequest(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_CHECKTEXTFORMATREQUEST, msg)

    text_length = unpack('I', parsed_msg[0:4])[0]
    text = parsed_msg[4:]

    if text_length != len(text):
        raise Error('Parsed text length %i not what expected %i' %
                    (text_length, len(text)))

    return text


def generate_checktextformatresponse(ret, width, height, last_index):
    return generate_message(TUI_MSGTYPE_CHECKTEXTFORMATRESPONSE,
                            pack('IIII', ret, width, height, last_index))


def parse_checktextformatresponse(msg):
    return unpack('IIII',
                  parse_message_of_type(TUI_MSGTYPE_CHECKTEXTFORMATRESPONSE, msg))


def generate_getscreeninforequest(orientation, numberofentryfields):
    return generate_message(TUI_MSGTYPE_GETSCREENINFOREQUEST,
                            pack('II', orientation, numberofentryfields))


def parse_getscreeninforequest(msg):
    return unpack('II',
                  parse_message_of_type(TUI_MSGTYPE_GETSCREENINFOREQUEST, msg))


fmt_getscreeninforesponse_first_segment = 'IIIIIIIIBBBII'
fmt_getscreeninforesponse_buttoninfo = 'IIBB'


def generate_getscreeninforesponse(ret,
                                   grayscalebitsdepth,
                                   redbitsdepth,
                                   greenbitsdepth,
                                   bluebitsdepth,
                                   widthinch,
                                   heightinch,
                                   maxentryfields,
                                   labelcolor,
                                   labelwidth,
                                   labelheight,
                                   buttoninfos):
    first_segment = pack(fmt_getscreeninforesponse_first_segment,
                         ret,
                         grayscalebitsdepth,
                         redbitsdepth,
                         greenbitsdepth,
                         bluebitsdepth,
                         widthinch,
                         heightinch,
                         maxentryfields,
                         labelcolor[0],
                         labelcolor[1],
                         labelcolor[2],
                         labelwidth,
                         labelheight)

    if len(buttoninfos) != 6:
        raise Error('Need 6 button infos')

    buttoninfo_segments = map(lambda x: generate_lengthvalue(x[0]) +
                              pack(fmt_getscreeninforesponse_buttoninfo,
                                   x[1],
                                   x[2],
                                   int(x[3]),
                                   int(x[4])),
                              buttoninfos)

    return generate_message(TUI_MSGTYPE_GETSCREENINFORESPONSE,
                            first_segment + ''.join(buttoninfo_segments))


def parse_getscreeninforesponse(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_GETSCREENINFORESPONSE, msg)

    first_segment_size = calcsize(fmt_getscreeninforesponse_first_segment)

    # Unpack values from the first segment
    v = unpack(fmt_getscreeninforesponse_first_segment,
               parsed_msg[0:first_segment_size])

    def parse_buttoninfo_segments(seg):
        button_text_length, button_text = parse_lengthvalue(seg)
        buttoninfo_size = calcsize('I') + button_text_length + \
                          calcsize(fmt_getscreeninforesponse_buttoninfo)
        seg_next = seg[buttoninfo_size:]

        buttonwidth, buttonheight, buttontextcustom, buttonimagecustom = \
            unpack(fmt_getscreeninforesponse_buttoninfo,
                   seg[calcsize('I') + button_text_length:buttoninfo_size])

        buttoninfo = (button_text,
                      buttonwidth,
                      buttonheight,
                      buttontextcustom != 0,
                      buttonimagecustom != 0)

        if len(seg_next) == 0:
            return (buttoninfo,)
        else:
            return (buttoninfo,) + parse_buttoninfo_segments(seg_next)


    return v[0:8] + (v[8:11],) + v[11:] + \
           (parse_buttoninfo_segments(parsed_msg[first_segment_size:]),)


def generate_initsessionrequest():
    return generate_message(TUI_MSGTYPE_INITSESSIONREQUEST, '')


def parse_initsessionrequest(msg):
    parse_message_of_type(TUI_MSGTYPE_INITSESSIONREQUEST, msg)


def generate_initsessionresponse(ret):
    return generate_message(TUI_MSGTYPE_INITSESSIONRESPONSE,
                            pack('I', ret))


def parse_initsessionresponse(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_INITSESSIONRESPONSE, msg)

    return unpack('I', parsed_msg)[0]


def generate_closesessionrequest():
    return generate_message(TUI_MSGTYPE_CLOSESESSIONREQUEST, '')


def parse_closesessionrequest(msg):
    parse_message_of_type(TUI_MSGTYPE_CLOSESESSIONREQUEST, msg)


def generate_closesessionresponse(ret):
    return generate_message(TUI_MSGTYPE_CLOSESESSIONRESPONSE,
                            pack('I', ret))


def parse_closesessionresponse(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_CLOSESESSIONRESPONSE, msg)

    return unpack('I', parsed_msg)[0]


def generate_displayscreenrequest(screenorientation,
                                  label,
                                  buttons,
                                  requestedbuttons,
                                  closetuisession,
                                  entryfields):

    def generate_image(img):
        return generate_lengthvalue(img[0]) + \
               pack('II', img[1], img[2])


    def generate_button(btn):
        return generate_lengthvalue(btn[0]) + \
               generate_image(btn[1])


    def generate_entryfield(ef):
        return generate_lengthvalue(ef[0]) + \
               pack('IIII', *ef[1:5])

    label_segment = generate_lengthvalue(label[0]) + \
                    pack('IIBBB',
                         label[1],
                         label[2],
                         label[3][0],
                         label[3][1],
                         label[3][2]) + \
                    generate_image(label[4]) + \
                    pack('II', label[5], label[6])
    buttons_segment = map(generate_button, buttons)
    reqbuttons_segment = pack('IIIIII', *map(int, requestedbuttons))
    entryfields_segment = map(generate_entryfield, entryfields)

    msg = pack('I', screenorientation) + \
          label_segment + \
          ''.join(buttons_segment) + \
          reqbuttons_segment + \
          pack('I', int(closetuisession)) + \
          pack('I', len(entryfields)) + \
          ''.join(entryfields_segment)

    return generate_message(TUI_MSGTYPE_DISPLAYSCREENREQEUST, msg)


def parse_displayscreenrequest(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_DISPLAYSCREENREQEUST, msg)

    screenorientation = unpack('I', parsed_msg[0:calcsize('I')])
    index = calcsize('I')

    def parse_image(imgmsg):
        img_size, img_data = parse_lengthvalue(imgmsg)
        img_size += calcsize('I')

        img_vals = unpack('II', imgmsg[img_size:img_size + calcsize('II')])

        return (img_data,) + img_vals, img_size + calcsize('II')


    def parse_label(lblmsg):
        text_length, text = parse_lengthvalue(lblmsg)
        index = text_length + calcsize('I')

        lbl1 = unpack('IIBBB', lblmsg[index:index + calcsize('IIBBB')])
        index += calcsize('IIBBB')

        lblimage, imgsize = parse_image(lblmsg[index:])
        index += imgsize

        lbl2 = unpack('II', lblmsg[index:index + calcsize('II')])
        index += calcsize('II')

        return (text, lbl1[0], lbl1[1], (lbl1[2], lbl1[3], lbl1[4])) + \
               (lblimage,) + lbl2, \
               index


    def parse_buttons(btnmsg):
        index = 0
        buttons = []

        for i in xrange(0,6):
            text_length, text = parse_lengthvalue(btnmsg[index:])
            index += text_length + calcsize('I')

            img, imgsize = parse_image(btnmsg[index:])
            index += imgsize

            buttons += ((text,) + (img,),)

        return tuple(buttons), index


    def parse_entryfields(efmsg, count):
        index = 0
        efs = []

        for i in xrange(0, count):
            text_length, text = parse_lengthvalue(efmsg[index:])
            index += text_length + calcsize('I')

            values = unpack('IIII', efmsg[index:index + calcsize('IIII')])
            index += calcsize('IIII')

            efs += ((text,) + values,)

        return tuple(efs)

    label, label_size = parse_label(parsed_msg[index:])
    index += label_size

    buttons, buttons_size = parse_buttons(parsed_msg[index:])
    index += buttons_size

    reqbuttons = map(lambda x: x != 0,
                     unpack('IIIIII',
                            parsed_msg[index:index + calcsize('IIIIII')]))
    index += calcsize('IIIIII')

    closetuisession = \
        unpack('I', parsed_msg[index:index + calcsize('I')])[0] != 0
    index += calcsize('I')

    entryfieldcount = unpack('I', parsed_msg[index:index + calcsize('I')])[0]
    index += calcsize('I')

    entryfields = parse_entryfields(parsed_msg[index:], entryfieldcount)


    return screenorientation + \
           (label,) + \
           (buttons,) + \
           (tuple(reqbuttons),) + \
           (closetuisession,) + \
           (entryfields,)


def generate_displayscreenresponse(ret, button, entryfields):
    first_segment = pack('III', ret, button, len(entryfields))
    entryfield_segments = map(lambda x: generate_lengthvalue(x), entryfields)

    return generate_message(TUI_MSGTYPE_DISPLAYSCREENRESPONSE,
                            first_segment + ''.join(entryfield_segments))


def parse_displayscreenresponse(msg):
    parsed_msg = parse_message_of_type(TUI_MSGTYPE_DISPLAYSCREENRESPONSE, msg)
    first_segment_size = calcsize('III')
    first_segment = parsed_msg[0:first_segment_size]
    entryfield_segments = parsed_msg[first_segment_size:]

    def parse_entryfields(seg):
        bufferlen = unpack('I', seg[0:4])[0]
        data = seg[4:4+bufferlen]
        seg_next = seg[4+bufferlen:]

        if len(seg_next) == 0:
            return (data,)
        else:
            return (data,) + parse_entryfields(seg_next)


    ret, button, entryfield_count = unpack('III', first_segment)
    entryfields = parse_entryfields(entryfield_segments)

    if len(entryfields) != entryfield_count:
        raise Error('entryfield_count differs from actual entry fields')

    return (ret, button, entryfields)
