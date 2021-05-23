#!/usr/bin/env sh
set -e
[ -d vendor ] || bundle install --path vendor/bundle

EXTERNAL_IP=$(curl -s "https://ipv4.icanhazip.com")
printf "# Managed by configure.sh\nallowed_ip = \"%s\"\n" "${EXTERNAL_IP}" > ./terraform/terraform.tfvars

# I would prefer to use ed25519, but AWS EC2 key pairs do not support ed25519 yet
# Passphrase intentionally left blank to make it available to Test Kitchen
[ -f "id_rsa" ] || ssh-keygen -t rsa -f id_rsa -N "" -C "test-kitchen"

(cd terraform; [ -d .terraform ] || terraform init)
echo "Running terraform apply..."
(cd terraform; terraform apply)

AWS_SUBNET_ID=$(cd terraform; terraform output -raw test_kitchen_subnet)
AWS_SECURITY_GROUP_ID=$(cd terraform; terraform output -raw test_kitchen_sg)
AWS_KEYPAIR_ID=$(cd terraform; terraform output -raw key_pair_id)
sed -i '' \
  -e "s/^.*subnet_id:.*/  subnet_id: \"${AWS_SUBNET_ID}\" # managed by configure.sh/" \
  -e "s/^.*security_group_ids:.*/  security_group_ids: [ \"${AWS_SECURITY_GROUP_ID}\" ] # managed by configure.sh/" \
  -e "s/^.*aws_ssh_key_id:.*/  aws_ssh_key_id: \"${AWS_KEYPAIR_ID}\" # managed by configure.sh/" \
  kitchen.yml

