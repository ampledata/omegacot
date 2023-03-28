#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Greg Albrecht <oss@undef.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""OmegaCoT Class Definitions."""

import asyncio
import json
import os

from typing import Optional

import pytak
import omegacot

__author__ = "Greg Albrecht <oss@undef.net>"
__copyright__ = "Copyright 2023 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


class OmegaWorker(pytak.QueueWorker):
    """Omega Cursor on Target Class."""

    async def handle_data(self, data) -> None:
        """Handle received GPS Info data."""
        event: Optional[bytes] = omegacot.omega_to_cot(data, self.config)
        if event:
            await self.put_queue(event)

    async def get_gps_info(self) -> None:
        """Get GPS Info data."""
        with os.popen(self.gps_info_cmd) as gps_info_cmd:
            _gps_info = gps_info_cmd.read()

        self._logger.debug("GPS_INFO=%s", _gps_info)
        gps_info = json.loads(_gps_info)
        await self.handle_data(gps_info)

    async def run(self, number_of_iterations=-1) -> None:
        """Run this Thread, reads GPS Info & outputs CoT."""
        self._logger.info("Sending to: %s", self.config.get("COT_URL"))

        poll_interval: int = int(
            self.config.get("POLL_INTERVAL", omegacot.DEFAULT_POLL_INTERVAL)
        )
        self.gps_info_cmd = self.config.get("GPS_INFO_CMD") or omegacot.DEFAULT_GPS_INFO_CMD

        while 1:
            await self.get_gps_info()
            self._logger.info("Polling every %ss: %s", poll_interval, self.gps_info_cmd)
            await asyncio.sleep(poll_interval)
