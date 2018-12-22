# downer
Wrapper around requests module to be used for downloading

Usage:
downer.download(_list of pairs_<, options>)
where pairs is a list of (_url_, _filename_) pairs
The contents of requets.get(_url_) will be written to _filename_
