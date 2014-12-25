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
#include <stdlib.h>

#define TUI_MSG_HEADER_SIZE (2 * sizeof(uint32_t))

enum tui_msg_type {
	TUI_MSGTYPE_CHECKTEXTFORMAT = 1,
	TUI_MSGTYPE_GETSCREENINFO,
	TUI_MSGTYPE_INITSESSION,
	TUI_MSGTYPE_CLOSESESSION,
	TUI_MSGTYPE_DISPLAYSCREEN
};

#endif /* __TUI_PROTOCOL_H__ */
