# pcapfex
'**P**acket **CAP**ture **F**orensic **E**vidence e**X**tractor' is a tool 
that finds and extracts files from packet capture files.

It was developed by _Viktor Winkelmann_ as part of a bachelor thesis.

The power of _pcapfex_ lies in it's ease of use. You only provide it a
pcap-file and are rewarded a structured export of all files found in it.
_pcacpfex_ allows data extraction even if non-standard protocols were used. 
It's easy to understand plugin-system offers python developers a quick way 
to add more file-types, encodings or
even complex protocols.

### Requirements
_pcapfex_ was developed and tested for **Linux environments only**.
Due to missing optimizations and tests, there is no guarantee for it to work
under Windows (though it should work).

_pcapfex_ depends on **Python 2.7** and the **_dpkt_** package. You can install 
it via
```
sudo pip install dpkt
```

To achieve better performance using a multithreaded search for file objects, you
should install the _regex_ package.
```
sudo pip install regex
```
However, this step is only optional.


### Usage
To analyze a pcap-file ```samplefile.pcap``` just use
```
pcapfex.py samplefile.pcap
```


For more detailed usage information see
```
pcapfex.py -h
```

Please make sure to use the ```-nv``` flag, if the machine
that captured the traffic was sending data as well. This will
circumvent wrong checksums stored in the pcap-file caused by
TCP-Checksum-Offloading.

### License
_pcapfex_ is published under the Apache 2.0 license.