## Silver Cpay App

This is a django app for integrating a Cpay into Silver. 

### Integration

The module can work both by invoking the api endpoints, or usign and overriding the django HTML templates

#### API Endpoint

Generate Parameters `POST /parameters`

Returns all the cpay parameters needed to generate a payment form. Generates a `Payment_Request` instance with all the data.

Expected POST variables:
- `invoice_ids` - comma separated list of valid Invoice Ids
- `proforma_ids` - comma separated list of valid Proforma Ids
- `redirect_ok_url` - a URL that the user will be redirected to at the end of the process if the transaction is successfull
- `redirect_fail_url` - a URL that the user will be redirected to at the end of the process if the transaction has failed
- `transaction_details` - a description for the transaction

implemented in `views.Cpay_View_Set.generate_parameters`

#### Django Views and Templates

