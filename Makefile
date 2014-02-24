#
# Targets:
#  - clean	Delete .pyc files

# Clean the working directory
clean:
	find . -name *.pyc -delete
	find . -name __pycache__ -delete
