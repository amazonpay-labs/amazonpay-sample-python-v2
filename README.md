# Amazon Pay API Sample Code (Python)

This Sample Code will allow you to integrate your application with the Amazon Pay v2 API.

# Setup

## clone

```
https://github.com/amazonpay-labs/amazonpay-sample-python-v2.git
cd amazonpay-sample-python-v2
```

## install dependencies of Python modules

```
# Install Crypt for sign
pip install -U PyCryptodome
```

This sample code use the following modules.

* LWP::UserAgent
* URI::Split qw(uri_split)
* JSON::PP
* Digest::SHA qw(sha256_hex)
* Crypt::PK::RSA
* MIME::Base64 qw(encode_base64)
* URI::Escape
* DateTime


# Functions
## Configurations

Before issuing any API call, you will create HTTP headers such as x-amz-pay-date, authorization & x-amz-pay-idempotency-key. You can use this following code samples to get signature for calling the Amazon Checkout v2 API.

```
    # Configurations
    method = 'GET' # POST/PATCH/DELETE
    accept = 'application/json'
    canonical_uri = '/v2/checkoutSessions/xxxxx-xxx-xx-xx-xxxx' # Change URI based on your API
    public_key = 'PUBLIC_KEY' # Enter you public key ID
    private_key = RSA.importKey(open('private.pem').read()) # Enter you private key file path
```

## Generate Signature For GET API

```

def generate_signature_for_GET_API() :
    # Note : Below Code is to create Signature for Get Checkout Session API, please change accordingly for other API's
    # Configurations
    method = 'GET'
    accept = 'application/json'
    canonical_uri = '/v2/checkoutSessions/xxxxx-xxx-xx-xx-xxxx' # Change URI based on your API
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
    signature = get_signature(string_to_sign, private_key)

    # Printing the HTTP Headers
    print_http_headers(accept, amz_pay_date, public_key, signed_headers, signature, '', '')

generate_signature_for_GET_API()
```

## Generate Signature For API's (POST, PATCH & DELETE)

```
    # Note : Below Code is to create Signature for Create Checkout Session API, please change accordingly for other API's
    # Configurations
    method = 'POST' # Change Method as PATCH & DELETE based on API
    accept = 'application/json'
    content_type = 'application/json'
    idempotencyKey = str(uuid.uuid4().hex) # idempotencyKey is applicable only for API's (Create Checkout Session, Create Charge, Capture Charge & Create Refund), plese remove this paramter for other API's
    canonical_uri = '/v2/checkoutSessions/' # Change URI based on your API
    public_key = 'PUBLIC_KEY' # Enter you public key ID
    private_key = RSA.importKey(open('private.pem').read()) # Enter you private key file path
    payload_json = '{"webCheckoutDetails":{"checkoutReviewReturnUrl":"https://amazon.com/store/checkout_review"},"storeId":"amzn1.application-oa2-client.xxxxxxxxxx"}' # Enter your API request payload

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
    signature = get_signature(string_to_sign, private_key)

    # Printing the HTTP Headers
    print_http_headers(accept, amz_pay_date, public_key, signed_headers, signature, idempotencyKey, content_type)
    
generate_signature_for_API()
```

## Other functions
Please check the [testrun.pl](https://github.com/amazonpay-labs/amazonpay-sample-perl-v2/blob/main/testrun.pl)

# Sample Output 
```
Generated HTTP Headers :
accept : application/json
x-amz-pay-date : 20211001T121153Z
authorization : AMZN-PAY-RSASSA-PSS-V2 PublicKeyId=PUBLIC_KEY, SignedHeaders=accept;content-type;x-amz-pay-date;x-amz-pay-idempotency-key, Signature=C5jR6a+ZCLkSwHBzBQocnq+dujL8To+HEgpH7jWVU95e56M8onZZH78Sspm1zIuSggRZDTtmUmPxJg/w4tY5XIeLHDjAGB+I5FDwlBdUScuD+0F9E8h2xrJUTS2L0zsc5VIAvlvgsGQtznTJc/3zWutNyZn169SEaJm6Yma6c7U=
x-amz-pay-idempotency-key : dc849a72e7194353a544579c905e20b6
content-type : application/json

```

# license
Licensed under the Apache License, Version 2.0 (the “License”).
