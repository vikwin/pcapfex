# pcapfex
'**P**acket **CAP**ture **F**orensic **E**vidence e**X**tractor' is a tool that finds and extracts files
from packet capture files.

It was developed by Viktor Winkelmann as part of a bachelor thesis.

The power of _pcapfex_ lies in it's ease of use. You only provide it a
pcap-file and are rewarded a structured export of all files found in it.
_pcacpfex_ offers modules, that allow data extraction even if
non-standard protocols are used. It's easy to understand plugin-system
offers python developers a quick way to add more file-types, encodings or
even complex protocols.

See _'pcapfex.py -h'_ for usage information.

_pcapfex_ is published under the Apache 2.0 license.