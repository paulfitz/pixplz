from __future__ import division

import argparse
from PIL import Image
import requests
import six
import sys
import re
import time
from tqdm import tqdm
from six.moves.urllib.parse import urlencode

MINIMUM_NUMBER_OF_IMAGES = 5


def get_cache_url(url):
    return "http://images.duckduckgo.com/iu/?{}".format(urlencode({'u': url}))


def get_urls(term):

    current_params = {
        'q': term,
        't': 'h_',
        'iax': 1,
        'ia': 'images'
    }
    result = requests.get("https://duckduckgo.com/",
                          params=current_params)
    m = re.search(r'vqd=\'([0-9]*)\'', result.text)
    vqd = m.group(1)
    current_params = {'l': 'us-en', 'o': 'json', 'q': term, 'f': ''}
    current_params['vqd'] = vqd

    accum = set()
    current_link = "i.js"

    for x in range(0, 100):
        if x > 0:
            time.sleep(5)
        result = requests.get("https://duckduckgo.com/{}".format(current_link),
                              params=current_params)
        result = result.json()
        current_params = {}
        chaff = [c['image'] for c in result['results']]
        for url in set(chaff) - accum:
            yield get_cache_url(url)
        accum |= set(chaff)
        if 'next' not in result:
            break
        current_link = result['next']


def get_images(args, urls):
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
                content = six.BytesIO(response.content)
                img = Image.open(content)
                img = img.convert('RGB')
                if args.format:
                    img.save(args.format % k)
                elif args.prefix:
                    img.save("%s%06d.jpg" % (args.prefix, k))
                k += 1
                pbar.update()
            except IOError:
                fails += 1
            if k >= args.count:
                break
    print("{} images downloaded ({} duds skipped)".format(k, fails))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('term', nargs='+',
                        help="search term")
    parser.add_argument('--prefix',
                        help="prefix for downloaded images, _NNNNNN.jpg will be added")
    parser.add_argument('--format',
                        help="format for naming images, for example 'foo/bar%%06d.png'")
    parser.add_argument('--parallel',
                        default=0,
                        type=int,
                        help="number of images to load in parallel (requires pixplz[parallel])")
    parser.add_argument('--count',
                        default=MINIMUM_NUMBER_OF_IMAGES,
                        type=int,
                        help="target number of images to load (fewer may be loaded)")
    args = parser.parse_args()
    urls = get_urls(' '.join(args.term))
    get_images(args, urls)


if __name__ == '__main__':
    main()
