#!/bin/sh
#    Copyright 2021 Thomas Bellebaum
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


# TODO verify the DSCList against the RKI List Signing Key
[ "$1" = "update" ] && curl "https://de.dscg.ubirch.com/trustList/DSC/" > DSC.json
[ "$1" = "update" ] && exit 0

video_device="$(find /dev/video* | head -n 1)" # Adjust to your needs
zbarcam --oneshot --raw "$video_device" | python dcc.py

