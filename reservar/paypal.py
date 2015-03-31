import urllib
import urllib2
def paypal_check(tx,at):
    success = False
    post_data = [('cmd','_notify-synch'),('tx',tx),('at',at)]     # a sequence of two element tuples
    result = urllib2.urlopen('https://www.sandbox.paypal.com/au/cgi-bin/webscr', urllib.urlencode(post_data))
    content = result.read().split('\n')
    results = {}

    for each in content[1:]:
        print each
        try:
            key, value = each.split("=")
            print key
            results[key] = value
        except:
            pass
    if content[0].find('SUCCESS') >= 0:
        success = True

    return success, results