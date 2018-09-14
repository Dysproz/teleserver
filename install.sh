sudo add-apt-repository ppa:ansible/ansible 
sudo apt-get update
sudo apt-get install -y ansible
wget "https://raw.githubusercontent.com/Dysproz/FlaskTVRemote/master/systemSetup.yml"
sudo ansible-playbook systemSetup.yml


