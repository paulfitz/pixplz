from __future__ import division

from PIL import Image
import requests
import six
import sys
import re
import time
from tqdm import tqdm
from six.moves.urllib.parse import urlencode
import grequests

MINIMUM_NUMBER_OF_IMAGES = 20


def get_cache_url(url):
    return "http://images.duckduckgo.com/iu/?{}".format(urlencode({'u': url}))


def get_urls(term, count=20):

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

    for x in range(0, 5):
        if x > 0:
            time.sleep(5)
        result = requests.get("https://duckduckgo.com/{}".format(current_link),
                              params=current_params)
        result = result.json()
        current_params = {}
        chaff = [c['image'] for c in result['results']]
        accum |= set(chaff)
        if 'next' not in result:
            break
        current_link = result['next']
        if len(accum) > count:
            break

    return list(get_cache_url(url) for url in accum)


def get_images(prefix, urls):
    responses = grequests.imap(grequests.get(u) for u in urls)
    k = 0
    fails = 0

    with tqdm(total=len(urls)) as pbar:
        for response in responses:
            try:
                content = six.BytesIO(response.content)
                img = Image.open(content)
                img = img.convert('RGB')
                img.save("%s_%06d.jpg" % (prefix, k))
                k += 1
            except IOError:
                fails += 1
            pbar.update()
    print("{} images downloaded, {} failed".format(k, fails))


def main():
    if len(sys.argv) < 3:
        print("Example: pixplz <prefix> <term>")
        print("Example: pixplz class1 car")
        exit(1)
    urls = get_urls(" ".join(sys.argv[2:]))
    get_images(sys.argv[1], urls)


if __name__ == '__main__':
    main()
