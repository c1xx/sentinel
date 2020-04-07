#!/bin/bash
set -evx

mkdir ~/.bitcorecore

# safety check
if [ ! -f ~/.bitcorecore/.bitcore.conf ]; then
  cp share/bitcore.conf.example ~/.bitcore/bitcore.conf
fi
