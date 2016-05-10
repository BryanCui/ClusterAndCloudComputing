echo "enter the number of instance: "
read -r NUM_INSTANCE

python boto_script.py $NUM_INSTANCE
source CCC-2016-5-openrc.sh
#nova list
swift upload twitter_container authorized_keys
swift upload twitter_container hosts
swift upload twitter_container twitter.py
swift upload twitter_container twitterApp.conf

ansible-playbook ansible.yaml -i hosts -u ubuntu --private-key=~/.ssh/id_rsa