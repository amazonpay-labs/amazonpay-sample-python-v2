# Make sure to install PyCryptodome before running the script
# Install PyCryptodome by using command pip install -U PyCryptodome
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import hashlib
import base64
import datetime 
import uuid

def hex_and_hash(data) :
    # Creating String to Sign
    return hashlib.sha256(data.encode('utf-8')).hexdigest() 

def get_date_time() :
    # Creating Date time stamp
    t = datetime.datetime.utcnow()
    return t.strftime('%Y%m%dT%H%M%SZ')

def get_to_string_to_sign(canonical_request) :
    return 'AMZN-PAY-RSASSA-PSS' + '\n' + hex_and_hash(canonical_request)

def get_siganture(string_to_sign, private_key) :
     # Calculating the Signature
    digest = SHA256.new(string_to_sign.encode('utf-8'))
    signer = PKCS1_PSS.new(private_key, None, 20)
    return base64.b64encode(signer.sign(digest))

def print_http_headers(accept, amz_pay_date, public_key, signed_headers, signature, idempotencyKey, content_type) :
    # Printing the HTTP Headers
    print('Generated HTTP Headers :')
    print('accept : ' + accept)
    print('x-amz-pay-date : ' + amz_pay_date)
    print('authorization : ' + 'AMZN-PAY-RSASSA-PSS PublicKeyId=' + public_key + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature.decode())
    if(idempotencyKey != '') :
        print('x-amz-pay-idempotency-key : ' + idempotencyKey)
    if(content_type != '') :
        print('content-type : ' + content_type)

def generate_signature_for_GET_API() :
    # Configurations
    method = 'GET'
    accept = 'application/json'
    canonical_uri = '/v2/checkoutSessions/f0048228-b817-4a29-b802-0f526fcc67d6' # Change URI based on your API
    public_key = 'PUBLIC_KEY' # Enter you public key ID
    private_key = RSA.importKey(open('private.pem').read()) # Enter you private key file path

    # Generating a canonical request
    canonical_querystring = ''
    amz_pay_date = get_date_time()
    canonical_headers = 'accept:' + accept + '\n' + 'x-amz-pay-date:' + amz_pay_date + '\n'
    signed_headers = 'accept;x-amz-pay-date'
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + hex_and_hash('')

    # Creating a String to Sign
    string_to_sign = get_to_string_to_sign(canonical_request)

    # Calculating the Signature
    signature = get_siganture(string_to_sign, private_key)

    # Printing the HTTP Headers
    print_http_headers(accept, amz_pay_date, public_key, signed_headers, signature, '', '')

generate_signature_for_GET_API()

def generate_signature_for_API() :
    # Configurations
    method = 'POST' # Change Method as PATCH & DELETE based on API
    accept = 'application/json'
    content_type = 'application/json'
    idempotencyKey = str(uuid.uuid4().hex) # idempotencyKey is applicable only for API's (Create Checkout Session, Create Charge, Capture Charge & Create Refund), plese remove this paramter for other API's
    canonical_uri = '/v2/checkoutSessions/' # Change URI based on your API
    public_key = 'PUBLIC_KEY' # Enter you public key ID
    private_key = RSA.importKey(open('private.pem').read()) # Enter you private key file path
    payload_json = '{"webCheckoutDetails":{"checkoutReviewReturnUrl":"https://amazon.com/store/checkout_review"},"storeId":"amzn1.application-oa2-client.a78badb5525a49c2b61b114e973e84ba"}' # Enter your API request payload

    # Generating a canonical request
    canonical_querystring = ''
    amz_pay_date = get_date_time()

    # Note : x-amz-pay-idempotency-key is applicable only for API's (Create Checkout Session, Create Charge, Capture Charge & Create Refund), plese remove this paramter for other API's from below lines
    canonical_headers = 'accept:' + accept + '\n' + 'content-type:' + content_type + '\n' +  'x-amz-pay-date:' + amz_pay_date + '\n' + 'x-amz-pay-idempotency-key:' + idempotencyKey + '\n'
    signed_headers = 'accept;content-type;x-amz-pay-date;x-amz-pay-idempotency-key'
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + hex_and_hash(payload_json)

    # Creating a String to Sign
    string_to_sign = get_to_string_to_sign(canonical_request)

    # Calculating the Signature
    signature = get_siganture(string_to_sign, private_key)

    # Printing the HTTP Headers
    print_http_headers(accept, amz_pay_date, public_key, signed_headers, signature, idempotencyKey, content_type)

generate_signature_for_API()
