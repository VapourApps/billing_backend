import requests, json

class VACurrencyConverter(object):
    api_key = '82baab9cb0e6ea5a6060'
    base_url = 'https://free.currencyconverterapi.com/api/v6'

    def get_conversion_rate(self, from_currency, to_currency):
        # We are using free.currencyconverterapi.com, which expects a <CURRENCY1>_<CURRENCY2> argument (example: EUR_MKD)
        # Then it also returns the result in a json with this key (example: {"EUR_MKD" : 61.493684}
        conv_string = '%s_%s' % (from_currency, to_currency)

        url = self.base_url + '/convert'
        params = {'q' : conv_string, 'compact' : 'ultra', 'apiKey' : self.api_key}

        result = requests.get(url, params = params)
        result = json.loads(result.text)
        return result[conv_string]

    def convert(self, amount, from_currency, to_currency, date):
        convert_rate = self.get_conversion_rate(from_currency, to_currency)

        new_amount = amount * convert_rate
        return amount
