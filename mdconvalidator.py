#!/usr/bin/env python3
import os
import sys
import argparse
import logging
import tempfile
import shutil
from pathlib import Path

import pypandoc
from lxml import etree


DATAPATH = Path('.')
TEMPLATES = {
    'tei': DATAPATH / 'template' / 'mdconvalidator_tei.xml',
    'html': DATAPATH / 'template' / 'mdconvalidator.html',
}
CSL = DATAPATH / 'csl' / 'digital_humanities_abstracts.csl'
SCHEMAS = {
    'tei': DATAPATH / 'schema' / 'dhconvalidator.xsd'
}
EXT = {
    'tei': '.xml',
    'html': '.html',
    'pdf': '.pdf'
}
# TODO: Validation fails w/o publisher. Make this configurable.
PUBLISHER = 'Frederik Elwert, Ruhr University Bochum'
# Additional pdf params example: { 'pdf': ['-V', 'geometry:margin=1.5cm']}


class MDConvalidator:
    """
    Main class that handles conversion and validation of a Markdown document
    to TEI.

    """

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.tempdir = tempfile.TemporaryDirectory()
        self.use_citeproc = False

    def __repr__(self):
        return f'MarkdownConValidator:\n\tInput:\t{self.infile}\n'\
               f'\tOutput:\t{self.outfile}'

    def __str__(self):
        return f'MarkdownConValidator:\n\tInput:\t{self.infile}\n'\
               f'\tOutput:\t{self.outfile}'

    def _get_file_path(self, ext=None):
        file_path = Path(self.tempdir.name) / Path(self.outfile).name
        if ext:
            file_path = file_path.with_suffix(ext)
        return file_path

    def set_pandoc_path(self, pandoc_path='/usr/local/bin/pandoc'):
        os.environ.setdefault('PYPANDOC_PANDOC', pandoc_path)
        return 0

    def convalidate(self, formats=['tei', 'html'], validate=['tei'],
                    additional={'pdf': []}):
        # Convert into all given formats
        outfiles = {}
        for format_ in formats:
            try:
                outfiles[format_] = self.convert(format_, additional)
            except():
                print(f'Error on format {format_}.')
        # Validate given formats
        logging.info(f'OUTFILES: {outfiles}')
        for format_ in validate:
            try:
                self.validate(outfiles[format_], format_)
            except():
                print(f'Failed to validate {outfiles[format_]}.')
        # Copy infile
        # TODO: This uses different media paths than the extracted ones.
        # Maybe we should revise media handling to keep original file names.
        shutil.copy(self.infile, self.tempdir.name)
        # Pack as .dhc
        archive_tempdir = tempfile.TemporaryDirectory()
        archive_base = Path(archive_tempdir.name) / Path(self.outfile).stem
        archive = shutil.make_archive(archive_base,
                                      'zip',
                                      self.tempdir.name)
        shutil.copyfile(archive, self.outfile)

    def convert(self, format_, additional):
        # Use infile directory as base for image paths and other resources
        basedir = Path(self.infile).parent
        logging.info(f'BASEDIR: {basedir}')
        # We want relative paths for the media.
        # Hence, we have to pass a relative path to pandoc, and not a
        # child of self.tempdir.
        # This means it creates the media folder inside the current directory.
        # We make sure this does not override any existing directories.
        mediadir = mediadirbase = 'Pictures'
        mediadircounter = 1
        while Path(mediadir).exists():
            mediadir = f'{mediadirbase}{mediadircounter}'
            mediadircounter += 1
        # Common pipeline
        pandoc_filters = [
        ]
        if self.use_citeproc:
            pandoc_filters.append('pandoc-citeproc')
        pandoc_args = [
            '--standalone',
            f'--extract-media={mediadir}',
            f'--csl={CSL}',
            f'--variable=publisher:"{PUBLISHER}"',
            f'--resource-path={basedir}',
        ]
        if format_.lower() == 'pdf':
            if 'pdf' in additional:
                for each in additional['pdf']:
                    pandoc_args.append(each)
        # Check if a custom template is configured
        if format_ in TEMPLATES:
            template = TEMPLATES[format_]
            pandoc_args.append(f'--template={template}')
        # Get file name
        outfile = self._get_file_path(EXT[format_])
        # Do the conversion
        logging.info(f'OUTFILE: {outfile}')
        logging.info(f'INFILE: {self.infile}')
        pypandoc.convert_file(self.infile,
                              to=format_,
                              extra_args=pandoc_args,
                              filters=pandoc_filters,
                              outputfile=f'{outfile}')
        logging.info(f'Converted {self.infile} to {outfile}.')
        # Move the media dir to tempdir.
        if Path(mediadir).exists():
            dst = Path(self.tempdir.name) / mediadir
            # Check if dst exsits, might already be present from
            # previous conversion.
            if not dst.exists():
                shutil.copytree(mediadir, dst)
            shutil.rmtree(mediadir)
        return outfile

    def validate(self, file_, format_):
        doctree = etree.parse(str(file_))
        schematree = etree.parse(str(SCHEMAS[format_]))
        schema = etree.XMLSchema(schematree)

        schema.assertValid(doctree)
        logging.info(f'Generated {format_} document is valid.')

    def get_pandoc_info(self):
        print(f'Pandoc version:\t{pypandoc.get_pandoc_version()}\n'
              f'Pandoc path:\t{pypandoc.get_pandoc_path()}\n'
              f'Pandoc formats:\t{pypandoc.get_pandoc_formats()}')


def main():
    # Parse commandline arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--verbose', action='store_true')
    arg_parser.add_argument('infile')
    arg_parser.add_argument('outfile')
    arg_parser.add_argument('use_citeproc')
    args = arg_parser.parse_args()
    # Set up logging
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.ERROR
    logging.basicConfig(level=level)
    # Return exit value
    mdc = MDConvalidator(args.infile, args.outfile)
    if bool(args.use_citeproc):
        mdc.use_citeproc = True
    mdc.convalidate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
