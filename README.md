# billing_backend
Django backend for subscription based billing

Instalation:
  
```bash
#1. Install curl, git and pip3
apt-get install -y curl git python3-pip

#2. Install virtualenv
pip3 install virtualenv

#3. Clone the repo
git clone https://github.com/VapourApps/billing_backend.git
cd billing_backend

#3.5 (Optional, but recommended) create a virtualenv
virtualenv va_billing_venv
source va_billing_venv/bin/activate

#4. (Optional) Edit various settings files
# You can skip this step before production, but you need to eventually edit these files
#  va_purchase_project/
#  ├── braintree_id.py.example
#  ├── cpay_settings.py.example
#  ├── db_settings.py.example
#  ├── email_settings.py.example
#  ├── va_settings.py.example

#5. Rename these to the proper files
for x in 'braintree_id.py' 'cpay_settings.py' 'db_settings.py' 'email_settings.py' 'va_settings.py'; do cp va_purchase_project/$x.example va_purchase_project/$x; done

#6. Install requirements
pip3 install -r requirements.txt

#7. Migrate
python3 manage.py migrate

#8. (Optional) load initial data
python3 manage.py loaddata init_data/auth_user.json
python3 manage.py loaddata init_data/va_saas_data.json
python3 manage.py loaddata init_data/silver_data.json
python3 manage.py loaddata init_dada/silver_extensions_data.json
```
