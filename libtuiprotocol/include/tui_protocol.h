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

#ifndef __TUI_PROTOCOL_H__
#define __TUI_PROTOCOL_H__

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "tui_datatypes.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TUI_MSG_HEADER_SIZE (2 * sizeof(uint32_t))

enum {
	TUI_MSGTYPE_CHECKTEXTFORMATREQUEST = 0x01,
	TUI_MSGTYPE_CHECKTEXTFORMATRESPONSE = 0x02,
	TUI_MSGTYPE_GETSCREENINFOREQUEST = 0x03,
	TUI_MSGTYPE_GETSCREENINFORESPONSE = 0x04,
	TUI_MSGTYPE_INITSESSIONREQUEST = 0x05,
	TUI_MSGTYPE_INITSESSIONRESPONSE = 0x06,
	TUI_MSGTYPE_CLOSESESSIONREQUEST = 0x07,
	TUI_MSGTYPE_CLOSESESSIONRESPONSE = 0x08,
	TUI_MSGTYPE_DISPLAYSCREENREQEUST = 0x09,
	TUI_MSGTYPE_DISPLAYSCREENRESPONSE = 0x0A
};

struct checktextformatrequest {
	size_t text_length;
	char *text;
};

struct checktextformatresponse {
	uint32_t ret;
	uint32_t width;
	uint32_t height;
	uint32_t last_index;
};

struct getscreeninforequest {
	uint32_t orientation;
	uint32_t entryfield_count;
};

uint32_t calc_checktextformatrequest_size(struct checktextformatrequest *s);

uint32_t generate_checktextformatrequest(FILE *stream,
					 struct checktextformatrequest *s);

uint32_t generate_checktextformatresponse(FILE *stream,
		                          struct checktextformatresponse *s);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* __TUI_PROTOCOL_H__ */
