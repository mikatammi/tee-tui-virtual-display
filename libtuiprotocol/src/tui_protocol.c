/*****************************************************************************
** Copyright (C) 2014 Intel Corporation.                                    **
**                                                                          **
** Licensed under the Apache License, Version 2.0 (the "License");          **
** you may not use this file except in compliance with the License.         **
** You may obtain a copy of the License at                                  **
**                                                                          **
**      http://www.apache.org/licenses/LICENSE-2.0                          **
**                                                                          **
** Unless required by applicable law or agreed to in writing, software      **
** distributed under the License is distributed on an "AS IS" BASIS,        **
** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. **
** See the License for the specific language governing permissions and      **
** limitations under the License.                                           **
*****************************************************************************/

#include "tui_protocol.h"
#include <string.h>

static uint32_t fwrite_check(FILE *dest, void *src, size_t len)
{
	return len != fwrite(src, len, 1, dest);
}

static uint32_t write_msg_header(FILE *stream, uint32_t type, uint32_t size)
{
	if (fwrite_check(stream, &type, sizeof(uint32_t)) ||
	    fwrite_check(stream, &size, sizeof(uint32_t)))
		return 1;

	return 0;
}

uint32_t calc_checktextformatrequest_size(struct checktextformatrequest *s)
{
	return sizeof(uint32_t) + s->text_length;
}

uint32_t generate_checktextformatrequest(FILE *stream,
					 struct checktextformatrequest *s)
{
	if (stream == NULL || s == NULL)
		return 1;

	if (write_msg_header(stream,
			     TUI_MSGTYPE_CHECKTEXTFORMATREQUEST,
			     calc_checktextformatrequest_size(s)) ||
	    fwrite_check(stream, &s->text_length, sizeof(uint32_t)) ||
	    fwrite_check(stream, s->text, s->text_length))
		return 2;

	return 0;
}

uint32_t generate_checktextformatresponse(FILE *stream,
		                          struct checktextformatresponse *s)
{
	if (stream == NULL || s == NULL)
		return 1;

	if (write_msg_header(stream,
			     TUI_MSGTYPE_CHECKTEXTFORMATRESPONSE,
			     4 * sizeof(uint32_t)) ||
	    fwrite_check(stream, &s->ret, sizeof(s->ret)) ||
	    fwrite_check(stream, &s->width, sizeof(s->width)) ||
	    fwrite_check(stream, &s->height, sizeof(s->height)) ||
	    fwrite_check(stream, &s->last_index, sizeof(s->last_index)))
		return 2;

	return 0;
}

uint32_t generate_getscreeninforequest(FILE *stream,
				       struct getscreeninforequest *s)
{
	if (stream == NULL || s == NULL)
		return 1;

	if (write_msg_header(stream,
			     TUI_MSGTYPE_DISPLAYSCREENREQEUST,
			     2 * sizeof(uint32_t)) ||
	    fwrite_check(stream, &s->orientation, sizeof(s->orientation)) ||
	    fwrite_check(stream, &s->entryfield_count, sizeof(s->entryfield_count)))
		return 2;

	return 0;
}

// TODO: Implement calculation function
//			     (12 * sizeof(uint32_t)) +
//			     (3 * sizeof(uint8_t)) +
//			     (6 * ())

uint32_t generate_getscreeninforesponse(FILE *stream,
					TEE_TUIScreenInfo *s)
{
	if (stream == NULL || s == NULL)
		return 1;

	if (write_msg_header(stream,
			     TUI_MSGTYPE_DISPLAYSCREENRESPONSE,
			     0) ||
	    fwrite_check(stream, &s->grayscaleBitsDepth, sizeof(s->grayscaleBitsDepth)) ||
	    fwrite_check(stream, &s->redBitsDepth, sizeof(s->redBitsDepth)) ||
	    fwrite_check(stream, &s->greenBitsDepth, sizeof(s->greenBitsDepth)) ||
	    fwrite_check(stream, &s->blueBitsDepth, sizeof(s->blueBitsDepth)) ||
	    fwrite_check(stream, &s->widthInch, sizeof(s->widthInch)) ||
	    fwrite_check(stream, &s->heightInch, sizeof(s->heightInch)) ||
	    fwrite_check(stream, &s->maxEntryFields, sizeof(s->maxEntryFields)) ||
	    fwrite_check(stream, &s->entryFieldLabelWidth, sizeof(s->entryFieldLabelWidth)) ||
	    fwrite_check(stream, &s->entryFieldLabelHeight, sizeof(s->entryFieldLabelHeight)) ||
	    fwrite_check(stream, &s->maxEntryFieldLength, sizeof(s->maxEntryFieldLength)) ||
	    fwrite_check(stream, &(s->labelColor[0]), sizeof(s->labelColor[0])) ||
	    fwrite_check(stream, &(s->labelColor[1]), sizeof(s->labelColor[1])) ||
	    fwrite_check(stream, &(s->labelColor[2]), sizeof(s->labelColor[2])) ||
	    fwrite_check(stream, &s->labelWidth, sizeof(s->labelWidth)) ||
	    fwrite_check(stream, &s->labelHeight, sizeof(s->labelHeight)))
		return 2;

	for (size_t i = 0; i < 6; ++i) {
		TEE_TUIScreenButtonInfo *b = &(s->buttonInfo[i]);
		uint32_t buttontext_length = strlen(b->buttonText);
		uint32_t btn_text_custom = b->buttonTextCustom;
		uint32_t btn_image_custom = b->buttonImageCustom;

		if (fwrite_check(stream, &buttontext_length, sizeof(buttontext_length)) ||
		    fwrite_check(stream, &b->buttonWidth, sizeof(b->buttonWidth)) ||
		    fwrite_check(stream, &b->buttonHeight, sizeof(b->buttonHeight)) ||
		    fwrite_check(stream, &btn_text_custom, sizeof(btn_text_custom)) ||
		    fwrite_check(stream, &btn_image_custom, sizeof(btn_image_custom)))
			return 2;
	}

	return 0;
}
