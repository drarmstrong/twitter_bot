This set of scripts is used for running the PDBe twitter bot (twitter.com/PDBimagebot), which periodically tweet images of structures from the PDB archive.

These scripts use the PDBe API get information on newly released entries and gets images from the public PDBe pages. It then uses the Twitter API to send these tweets directly from the @PDBimagebot Twitter account.

The 'secrets.py' file has been removed from this repository - this is required to tweet specifically from a particular Twitter account.
