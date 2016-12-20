#! /usr/bin/python2
import json
import sys
from jinja2 import Template, Environment, FileSystemLoader

config = {}

def render_template(name):
    template = env.get_template(name)
    return template.render(config)

if __name__ == '__main__':
    config_file = 'config.json'
    if len(sys.argv) > 1:
        config_file = ' '.join(sys.argv[1:])
    with open(config_file, 'r') as f:
        config = json.load(f)
    env = Environment(loader=FileSystemLoader(config['template_dir']))
    outdir = config['output_dir']
