#!/usr/bin/env bash

BASE="http://metadata.services.cityinthe.cloud:1338/latest/meta-data/network/interfaces/macs/0e:49:61:0f:c3:11"

curl -s $BASE/device-number
curl -s $BASE/interface-id
curl -s $BASE/ipv6s
curl -s $BASE/local-hostname
curl -s $BASE/local-ipv4s
curl -s $BASE/mac
curl -s $BASE/network-card-index
curl -s $BASE/owner-id
curl -s $BASE/public-hostname
curl -s $BASE/public-ipv4s
curl -s $BASE/security-group-ids
curl -s $BASE/security-groups
curl -s $BASE/subnet-id
curl -s $BASE/subnet-ipv4-cidr-block
curl -s $BASE/subnet-ipv6-cidr-blocks
curl -s $BASE/vpc-id
curl -s $BASE/vpc-ipv4-cidr-block
curl -s $BASE/vpc-ipv4-cidr-blocks
curl -s $BASE/vpc-ipv6-cidr-blocks
