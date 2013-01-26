import argparse

class Config:
    def __init__(self):
        self.verbose        = True
        self.test_results   = False
        self.test_precision = False
        self.print_imports  = False
        self.types_number   = 10
        self.params_parsed  = False

    def parse(self):
        parser = argparse.ArgumentParser(description='Python Type Inference Project.')
        parser.add_argument('filename', help='filename of python source')
        parser.add_argument('-V', '--verbose'  , action='store_true', help='verbose output')
        parser.add_argument('-t', '--test'     , action='store_true', help='test results'  )
        parser.add_argument('-p', '--precision', action='store_true', help='test precision')
        parser.add_argument('-i', '--imports'  , action='store_true', help='print imports' )
        parser.add_argument('-l', '--limit'    , type=int, default=10, help='limit number of types')
        args = parser.parse_args()
        self.verbose        = args.verbose
        self.test_results   = args.test
        self.test_precision = args.precision
        self.print_imports  = args.imports
        self.types_number   = args.limit
        self.params_parsed  = True

config = Config()
#if not config.params_parsed:
#    config.parse()