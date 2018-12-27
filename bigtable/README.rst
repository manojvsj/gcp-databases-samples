Setup
++++++++++++++

#. Clone the repository in your local machine.

    .. code-block:: bash

        $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git


#.  Create bigtable instance using terraform

Install terraform in your local machine 
refer: https://learn.hashicorp.com/terraform/getting-started/install.html

    .. code-block:: bash
        $ terraform -v

Give local file path of your service account secret key file in "vars.tfvars" to authenticate your GCP account

    .. code-block:: bash
        project_id = "my-project-id"
        service_account_key_path = "/etc/gcp_keys/secret_key.json"

    .. code-block:: bash
        $ cd gcloud-databases/bigtable/terraform

    .. code-block:: bash
        $ terraform init
        $ terraform plan -var-file=vars.tfvars
        $ terraform apply -var-file=vars.tfvars
        $ terraform destroy -var-file=vars.tfvars


terraform apply command will create the GCP resources based on your configuration. 




Authentication
++++++++++++++

This sample requires you to have authentication setup. Refer to the
`Authentication Getting Started Guide`_ for instructions on setting up
credentials for applications.

.. _Authentication Getting Started Guide:
    https://cloud.google.com/docs/authentication/getting-started

Install Dependencies
++++++++++++++++++++

#. Clone python-docs-samples and change directory to the sample directory you want to use.

    .. code-block:: bash

        $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

#. Install `pip`_ and `virtualenv`_ if you do not already have them. You may want to refer to the `Python Development Environment Setup Guide`_ for Google Cloud Platform for instructions.

   .. _Python Development Environment Setup Guide:
       https://cloud.google.com/python/setup

#. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.

    .. code-block:: bash
        $ cd gcloud-databases/bigtable/terraform
        $ virtualenv venv
        $ source venv/bin/activate

#. Install the dependencies needed to run the samples.

    .. code-block:: bash

        $ pip install -r requirements.txt

.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/

Samples
-------------------------------------------------------------------------------

Basic example
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: https://gstatic.com/cloudssh/images/open-btn.png
   :target: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=bigtable/hello/main.py,bigtable/hello/README.rst


To run this sample:

.. code-block:: bash

    $ python main.py -h

    usage: main.py [-h] [--table_id TABLE_ID] [--key_path KEY_PATH]

    Demonstrates how to connect to Cloud Bigtable and run some basic operations.
    Prerequisites: - Create a Cloud Bigtable cluster.
    https://cloud.google.com/bigtable/docs/creating-cluster - Set your Google
    Application Default Credentials.
    https://developers.google.com/identity/protocols/application-default-
    credentials
    
    optional arguments:
      -h, --help           show this help message and exit
      --table_id TABLE_ID  bigtable Table name (default: sample_table)
      --key_path KEY_PATH  path for your service account json file path (default:
                           None)
    
    
    
    $ python main.py --key_path=/etc/gcp_keys/secret-key.json
    
    $ python main.py #it will take default credentials