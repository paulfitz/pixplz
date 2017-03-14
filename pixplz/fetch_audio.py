from __future__ import division

import argparse
import os
from PIL import Image
import requests
import six
import re
import time
from tqdm import tqdm
from six.moves.urllib.parse import urlencode

MINIMUM_NUMBER_OF_PIECES = 5


def get_urls(term):

    current_params = {
        'q': term
    }
    # result = requests.get("https://www.freesound.org/search/",
    #                      params=current_params)

    accum = set()

    for x in range(1, 100):
        result = requests.get("https://www.freesound.org/search/",
                              params=current_params)

        paths = re.findall(r'data/previews/[0-9]+/[^.">]*.mp3', result.text)
        paths = set(paths) - accum
        for path in paths:
            yield os.path.join('https://www.freesound.org', path)
        accum = accum | paths

        time.sleep(5)

        current_params['page'] = x + 1


def get_media(args, urls):
    if args.parallel == 0:
        try:
            import grequests
            args.parallel = None
        except ImportError:
            args.parallel = 1
            pass
    if args.parallel != 1:
        try:
            import grequests
            responses = grequests.imap((grequests.get(u) for u in urls), size=args.parallel)
        except ImportError:
            print("Please do 'pip install pixplz[parallel]' to enable parallel loading")
            exit(1)
    else:
        responses = six.moves.map(requests.get, urls)
    k = 0
    fails = 0

    if not (args.format or args.prefix):
        args.prefix = '_'.join(args.term) + '_'

    with tqdm(total=args.count) as pbar:
        for response in responses:
            try:
                # content = six.BytesIO(response.content)
                if args.format:
                    with open(args.format % k, 'wb') as fout:
                        fout.write(response.content)
                elif args.prefix:
                    with open("%s%06d.mp3" % (args.prefix, k), 'wb') as fout:
                        fout.write(response.content)
                k += 1
                pbar.update()
            except IOError:
                fails += 1
            if k >= args.count:
                break
    print("{} mp3 files downloaded ({} duds skipped)".format(k, fails))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('term', nargs='+',
                        help="search term")
    parser.add_argument('--prefix',
                        help="prefix for downloaded audio, _NNNNNN.mp3 will be added")
    parser.add_argument('--format',
                        help="format for naming files, for example 'foo/bar%%06d.mp3'")
    parser.add_argument('--parallel',
                        default=0,
                        type=int,
                        help="number of files to load in parallel (requires pixplz[parallel])")
    parser.add_argument('--count',
                        default=MINIMUM_NUMBER_OF_PIECES,
                        type=int,
                        help="target number of audio files to load (fewer may be loaded)")
    args = parser.parse_args()
    urls = get_urls(' '.join(args.term))
    get_media(args, urls)


if __name__ == '__main__':
    main()
