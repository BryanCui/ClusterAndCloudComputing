echo "enter the number of instance: "
read -r NUM_INSTANCE
if (( NUM_INSTANCE > 0)); then
	continue
else
	printf "must enter a number and should be greater than 0\n"
	exit
fi

# sudo pip install boto
# sudo pip install python-swiftclient
# sudo pip install ansible
# sudo pip install --upgrade pbr
# sudo pip install python-keystoneclient
# sudo pip install markupsafe
# sudo apt-get install build-essential libssl-dev libffi-dev python-dev
# sudo pip install cryptography

python boto_script.py $NUM_INSTANCE

source ./CCC-2016-5-openrc.sh
#nova list
swift upload twitter_container authorized_keys
swift upload twitter_container hosts
swift upload twitter_container twitter.py
swift upload twitter_container twitterApp.conf
swift upload twitter_container harvest-twitter.conf

export ANSIBLE_HOST_KEY_CHECKING=False
sleep 15
ansible-playbook ansible.yaml -i hosts -u ubuntu --private-key=~/.ssh/id_rsa
