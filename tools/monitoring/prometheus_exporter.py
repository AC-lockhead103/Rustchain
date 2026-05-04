#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
RustChain Prometheus Exporter (tools edition)


Patched from LaplaceRC PR #1711, with infrastructure refs fixed.
For the simpler standalone exporter, see monitoring/rustchain-exporter.py.


This version adds:
  - Class-based architecture with configurable scrape intervals
  - CLI arguments (--node-url, --listen-port, --scrape-interval)
  - Per-endpoint response-time gauges
  - JSON config file support
  - Additional v2 metrics: api_requests_total, scrape_duration_seconds,
    epoch_block_time_avg, miner_antiquity_distribution, tx_pool_size
"""


import time
import logging
import argparse
import json
import os
from threading import Thread
from typing import Dict, Optional, Any


import requests
from prometheus_client import start_http_server, Gauge, Counter, Info, Histogram


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Configuration defaults — fixed to real RustChain infrastructure
