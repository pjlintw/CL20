"""Implement utilities."""

import os
import time
import yaml
import argparse
from pathlib import Path


def get_args():
    """Get Parser."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--config", type=str, default="config.yml")

    return parser.parse_args()


def load_config(args):
    """Load configuration ifle."""
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


def create_dir(path):
    """Savely creating recursive directories"""
    if not isinstance(path, Path):
        path = Path(path)

    if not os.path.exists(path):
        os.makedirs(path)
        print('Created directory: {}'.format(path))
    else:
        print('Directory {} already exists.'.format(path))
