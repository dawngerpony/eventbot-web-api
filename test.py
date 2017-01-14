import requests
import simplejson as json

BASE_URL = 'http://localhost:5000'

HEADERS = {
    'Content-Type': 'application/json'
}


# def test_webhook_application_form_old():
#     """ Test the webhook application form.
#     """
#     body = {
#         'foo': 'bar'
#     }
#     r = requests.post('{}/webhook/application_form'.format(BASE_URL), json.dumps(body), headers=HEADERS)
#     o = r.json()
#     print o
#     assert o['status'] == 'ok', o['status']


def test_webhook_application_form():
    """ Test the webhook application form.
    """
    payload = {
        'Field3': 'Dafydd'
    }
    r = requests.post('{}/webhook/application_form'.format(BASE_URL), data=payload)
    o = r.json()
    # print json.dumps(o, indent=2)
    assert o['status'] == 'ok', o['status']
    assert o['Field3']['data'] == 'Dafydd', o['Field3']['data']


# curl 'https://afterpandora.wufoo.com/forms/joining-form/' -H 'Cookie: optimizelyEndUserId=oeu1452526901929r0.564602738013491; SSLB=0; SSID=CAAVbh0AAAAAAAAzzZNWHYyDADPNk1YGAAAAAAAAAAAAdvdWWABNCw; SSSC=6.G6238555527773916189.6|0.0; SSRT=dvdWWAAAAA; SSPV=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA; PHPSESSID=oa8bivs7i9blrjdk6m0f3blbg1; optimizelySegments=%7B%222090021884%22%3A%22direct%22%2C%222096050962%22%3A%22gc%22%2C%222105222282%22%3A%22false%22%7D; optimizelyBuckets=%7B%227948833562%22%3A%227951623691%22%7D; __utma=95344282.1552934923.1452526902.1482094458.1484390753.7; __utmc=95344282; __utmz=95344282.1482094458.6.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ceg.s=ojrn8i; _ceg.u=ojrn8i; cvo_sid1=CX2Y5HQC72A2; cvo_tid1=A9hP3dc6jEM|1482094458|1484390764|0; wuSecureCookie=%82%9B%3Bc%10%99%D3%08%14%BF%BC%28%8C%28C%90; cfu=UserID%3D903440; afterpandora2=submitted; wuentry=e-52006-f102; endpage=%7B%22Username%22%3A%22afterpandora%22%2C%22FormHash%22%3A%22m7czf9w1qhkds7%22%7D; wuConfirmPage=0; ep201=pTW3NrM7Ay64QIF4OlCoTK23UXo=; ep202=SHPJTCDOQPZRWUBQ5wzOGdAjOxQ=' -H 'Origin: https://afterpandora.wufoo.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundarydzCOBaa8kgAv0pZC' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Referer: https://afterpandora.wufoo.com/forms/joining-form/' -H 'Connection: keep-alive' --data-binary $'------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field3"\r\n\r\nDafydd name\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field27"\r\n\r\nDafydd referral\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field5"\r\n\r\ndafydd@afterpandora.com\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field6"\r\n\r\nDuffX\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field8"\r\n\r\nFetlife\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field14"\r\n\r\nOther site\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field11"\r\n\r\nMyself\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field12"\r\n\r\nMy interests\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="Field17"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="recaptcha_challenge_field"\r\n\r\n03AHJ_Vuuzd0NtIiFdj2EwhRWO_tlpvgkqA1mTF_77tdo3QR2Oq0ILEzYBgLyw3ORwUJY8tvchaaOC_-B8ZE0B-iNkfEL5o9WJWjpOgt_4Lh59V54zHIhJCJsh-_gFgGoTtkkiG5SKz1DFny2fUPGO2IMIU4Z24iIzE9KViffVFDIAEIQ6LRZLXpc4tV_-Iz3Maah7HvcEaQ1Q\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="recaptcha_response_field"\r\n\r\ncalle bbva\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="currentPage"\r\n\r\nTgWvVaIL4icpQ0TO4EmVwuslash0RAw0OJSL8UOjIPTlzCQwuBew=\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="saveForm"\r\n\r\nApply!\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="comment"\r\n\r\n\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="idstamp"\r\n\r\nHN8H+ZbSbvbRdFMI0PeYCgfvWKGBuSxLjqjwl2Pb+sg=\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="stats"\r\n\r\n{"errors":0,"startTime":9302,"endTime":41933,"referer":"http://www.afterpandora.com/becoming-an-after-pandora-member"}\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC\r\nContent-Disposition: form-data; name="clickOrEnter"\r\n\r\nclick\r\n------WebKitFormBoundarydzCOBaa8kgAv0pZC--\r\n' --compressed
