# Silver Cpay App

This is a django app for integrating a Cpay into Silver. 

## Integration

The module can work both by invoking the api endpoints, or usign and overriding the django HTML templates

### API Endpoints

Generate Parameters `POST /parameters`

Returns all the cpay parameters needed to generate a payment form. Generates a `Payment_Request` instance with all the data.

Expected POST variables:
- `invoice_ids` - comma separated list of valid Invoice Ids
- `proforma_ids` - comma separated list of valid Proforma Ids
- `redirect_ok_url` - a URL that the user will be redirected to at the end of the process if the transaction is successfull
- `redirect_fail_url` - a URL that the user will be redirected to at the end of the process if the transaction has failed
- `transaction_details` - a description for the transaction

implemented in `views.Cpay_View_Set.generate_parameters`

### Django Views and Templates

Besides using the API endpoint for generating parameters, you can use the ready made view in `views.generate_cpay_form`.

An example with this view is done in `silver_extensions.views`

There are four views created outside fo the Silve Cpay App that utilize the functionality of the app:

- `silver_extensions.views.pay_select` 
- `silver_extensions.views.pay_confirm`
- `silver_extensions.views.cpay_payment_ok`
- `silver_extensions.views.cpay_payment_fail`

You can see the whole process, staring from this URL: `va_silver/pay_select`

### Models

The app comes with two models:

- **Payment_Request** - holds all the info about the cpay payment request. Created each time the `generate_cpay_parameters` is called. It is linked to related Invoices and Proformas with M:N relations

- **Notification** - holds all the info about Cpay success and failed notifiactions. Linked with the  Payment_Request that initiated the payment

### Settings

The app settings defined in `app_settings.py`. The required parameters need to be defined in `va_settings.py`
- `CPAY_MERCHANT_ID` - required, supplied by Casys
- `CPAY_MERCHANT_NAME` - required, supplied by Casys
- `CPAY_PASSWORD` - required, supplied by Casys. In the testing env, the password is `'TEST_PASS'`
- `CPAY_IS_TESTING` - optional, optional, `False` by default. Used to switch between cpay post production and test URLs. When set to `True` will force the `CPAY_PASSWORD` to be `'TEST_PASS'`
- `CPAY_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY` - optional, `False` by default. When set to true, will generate a `PaymentMethod` instance for every customer that tries to initiate a payment. Requires cpay do be added ad a payment processor in `settings.py`

### Silver Payment Methods, Processors and Transactions
The app is not done as a proper fully functional Silver Payment processor.

A tutorial for writing proper payment processors for silver is available here: https://www.presslabs.com/code/silver/guides/adding-a-new-payment-processor/

The app, as it is, has a dummy processor class in payment_processors.py. This class is added in `settings.py.` in the `PAYMENT_PROCESSORS` variable. This config will allow you to select cpay as a payment processor in the admin, but it is not fully functional.

A Payment processor is needed in order to create Payment Methods. Payment Methods are defined per Customer. The app is capable of creating payment methods for customers that don't have one. There is a settings varible that controls this: `CPAY_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY`

Payment Methods are need in order to use the Transactions. The Silver documentation defines a Transaction as: "a relation between a Document and a Payment Method". When a customer has a Payment Method defined, a Transaction with state Initial will be generated for every issued invoice. For customers without a Payment method, Silver does not generate transactions. The app does not handle transactions at all, it just marks the invoice as paid, whether it has a transaction or not.

A better understanding of the whole Silver Payment and Transaction process is needed in order to integrate this part properly.

Silver Docs on Transactions: https://www.presslabs.com/code/silver/resources/#transaction