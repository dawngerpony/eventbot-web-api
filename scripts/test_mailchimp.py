#!/usr/bin/env python
import logging

# import eventbot.integrations.mailchimp_client as mc

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import pprint
    import sys
    argv = sys.argv
    pp = pprint.PrettyPrinter(indent=4)
    # result = mc.search(argv[1], alldata=True)
    # pp.pprint(result)
