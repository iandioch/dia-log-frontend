#! /usr/bin/python2
import errno
import json
import os
import sys
from jinja2 import Template, Environment, FileSystemLoader

config = {}

def render_template(name):
    template = env.get_template(name)
    return template.render(config)

def generate_dir(inpath, outpath):
    print ('Generating dir "%s" in "%s"' % (inpath, outpath))
    #mkdir -p
    try:
        os.makedirs(outpath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(outpath):
            pass
        else:
            raise

    things = os.listdir(inpath) # both files and dirs
    for thing in things:
        full_path = inpath + '/' + thing
        print('Looking at "%s"' % full_path)
        if os.path.isdir(full_path):
            # recurse
            generate_dir(full_path, outpath + '/' + thing.split('/')[-1])
        elif len(thing) > 5 and thing[-5:] == '.html':
            # actually do the whole templating bit
            template_path = full_path[len(config['template_dir']):]
            print ('Rendering template "%s"' % template_path)
            out = render_template(template_path)
            with open(outpath + '/' + thing, 'wb') as f:
                f.write(out.encode('utf8'))
        else:
            # plain boring old file, copy it 
            print ('Copying file "%s"' % full_path)
            pass

if __name__ == '__main__':
    config_file = 'config.json'
    if len(sys.argv) > 1:
        config_file = ' '.join(sys.argv[1:])
    with open(config_file, 'r') as f:
        config = json.load(f)
    env = Environment(loader=FileSystemLoader(config['template_dir']))
    outdir = config['output_dir']
    generate_dir(config['template_dir'], outdir)
