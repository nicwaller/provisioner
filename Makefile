.PHONY: test
test:
	bundle exec kitchen converge all
	bundle exec kitchen verify all
