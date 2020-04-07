#!/bin/bash
set -evx

mkdir ~/.bitcorecore

# safety check
if [ ! -f ~/.bitcorecore/.bitcore.conf ]; then
  cp share/bitcore.conf.example ~/.bitcorecore/bitcore.conf
fi
