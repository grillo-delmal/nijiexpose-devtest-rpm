#!/usr/bin/bash

sed -i "s/%define nijiexpose_ver .*/%define nijiexpose_ver $1/" nijiexpose-nightly.spec
sed -i "s/%define nijiexpose_dist .*/%define nijiexpose_dist $2/" nijiexpose-nightly.spec
sed -i "s/%define nijiexpose_short .*/%define nijiexpose_short $3/" nijiexpose-nightly.spec
