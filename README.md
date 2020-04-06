# rbk_get_versions
A quick script to get/find versions of CDM for multiple Rubrik Clusters

The goal of this script is to find out versions of the CDM software across multiple Rubrik clusters.  In our internal
labs we have many clusters that get re-imaged regularly and I had the need to find specific versions for testing.  This
script is an attempt to automate that process.

The script takes an input file that can either be plaintext or encoded using the creds_encode script included as well.
The creds_encode script takes a text file and converts it into an encoded version of the data to hide credentials.  

Syntax of creds_encode:
<pre>
Usage: creds_encode.py input_file output_file
</pre>

Syntax of rbk_get_versions
<pre>
Usage: rbk_get_versions.py [-h] -c config | -i config [-f os_family
-h | --help: Prints this message
-c | --config: Use this file for hosts/creds (encoded)
-i | --input: Use this file for host/creds (plain textt)
-f | --find: Only show versions that start with given string
NOTE: -i or -c is required.
</pre>

The format of the config file is:
host:user:password

One host per line.

The -f flag is used to find a particular family of OS.  It does a simple match where it looks at the version of the Rubrik
cluster and matches the string you give as the argument from the beginning of the version string of the cluster.  So
-f 5.1 would match any version starting with 5.1.
