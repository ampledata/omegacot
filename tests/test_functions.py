#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Greg Albrecht <oss@undef.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""OmegaCoT Function Tests."""

import io
import xml.etree.ElementTree as ET

import pytest

from omegacot.functions import omega_to_cot, omega_to_cot_xml


__author__ = "Greg Albrecht <oss@undef.net>"
__copyright__ = "Copyright 2023 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


@pytest.fixture
def sample_gps_info():
    return {
        "age": "1",
        "latitude": "35.421299",
        "longitude": "-78.656219",
        "elevation": "40.4",
        "course": "274.1",
        "speed": "0.0"
    }


def test_omega_to_cot_xml(sample_gps_info):
    cot = omega_to_cot_xml(sample_gps_info)
    assert isinstance(cot, ET.Element)
    assert cot.tag == "event"
    assert cot.attrib["version"] == "2.0"
    assert cot.attrib["type"] == "a-u-G"
    # assert cot.attrib["uid"] == "MMSI-366892000"

    point = cot.findall("point")
    assert point[0].tag == "point"
    assert point[0].attrib["lat"] == "35.421299"
    assert point[0].attrib["lon"] == "-78.656219"
    assert point[0].attrib["hae"] == "9999999.0"

    detail = cot.findall("detail")
    assert detail[0].tag == "detail"

    track = detail[0].findall("track")
    assert track[0].attrib["course"] == "274.1"
    assert track[0].attrib["speed"] == "0.0"


def test_omega_to_cot(sample_gps_info):
    """Test converting Omega GPS Info to CoT."""
    cot: bytes = omega_to_cot(sample_gps_info)
    assert b"a-u-G" in cot
    assert b"OnionOmega" in cot
