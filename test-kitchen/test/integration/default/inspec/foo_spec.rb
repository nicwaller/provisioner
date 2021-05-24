describe user('www-data') do
  it { should exist }
  its('group') { should eq 'www-data' }
#   its('groups') { should eq ['root', 'other']}
#   its('home') { should eq '/root' }
#   its('shell') { should eq '/bin/bash' }
end

describe package('apache2') do
  it { should be_installed }
end

describe package('php') do
  it { should be_installed }
end

describe service('apache2') do
  it { should be_installed }
  it { should be_enabled }
  it { should be_running }
end

describe port(80) do
  it { should be_listening }
  its('processes') { should include 'apache2' }
  its('protocols') { should cmp 'tcp' }
end

describe port(443) do
  it { should_not be_listening }
end

describe file('/var/www/html/index.php') do
  it { should be_file }
  its('mode') { should cmp '0444' }
  its('owner') { should eq 'root' }
  its('content') { should match /<?php/ }
  its('size') { should be > 64 }
  it { should be_allowed('read', by_user: 'www-data') }
  it { should_not be_allowed('write', by_user: 'httpd') }
end

describe command('curl -s -o /dev/null --write-out "%{http_code}" http://localhost') do
  its('stdout') { should eq "200" }
  its('stderr') { should eq '' }
  its('exit_status') { should eq 0 }
end

describe command('curl -sv http://localhost') do
  its('stdout') { should match /Hello, world!/ }
  its('stderr') { should match /200 OK/ }
  its('exit_status') { should eq 0 }
end

describe command('apache2ctl configtest') do
  its('stdout') { should eq "" }
  its('stderr') { should match /Syntax OK/ }
  its('exit_status') { should eq 0 }
end


