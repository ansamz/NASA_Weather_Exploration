cd /opt
sudo wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
sudo tar xzf Python-3.9.6.tgz
cd Python-3.9.6
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.9.6.tgz

cd ~/

python -m pip install --user virtualenv

mkdir folder
cd folder
virtualenv v-env --python=python3.9
source ./v-env/bin/activate
pip install requests_cache          
pip install retry_requests
deactivate

mkdir python
cd python
cp -r ../v-env/lib/python3.9/site-packages/* .
cd ..
zip -r requests_layer.zip python
aws lambda publish-layer-version --layer-name requests_lambda_layer --zip-file fileb://requests_layer.zip --compatible-runtimes python3.9
