import logging

from .instance import set_shared_blockchain_instance, shared_blockchain_instance
from .chainspec import BitSharesNodeRPC


class InterfaceConnection:

    def __init__(self, node="", rpcuser="", rpcpassword="", **kwargs):

        # More specific set of APIs to register to
        if "apis" not in kwargs:
            kwargs["apis"] = [
                "database",
                "network_broadcast",
            ]
        self.rpc = None
        if not self.offline:
            self.connect(node=node,
                         rpcuser=rpcuser,
                         rpcpassword=rpcpassword,
                         **kwargs)

    # -------------------------------------------------------------------------
    # Basic Calls
    # -------------------------------------------------------------------------
    def connect(self,
                node="",
                rpcuser="",
                rpcpassword="",
                **kwargs):
        """ Connect to BitShares network (internal use only)
        """
        if not node:
            if "node" in self.config:
                node = self.config["node"]
            else:
                raise ValueError("A BitShares node needs to be provided!")

        if not rpcuser and "rpcuser" in self.config:
            rpcuser = self.config["rpcuser"]

        if not rpcpassword and "rpcpassword" in self.config:
            rpcpassword = self.config["rpcpassword"]

        self.rpc = BitSharesNodeRPC(node, rpcuser, rpcpassword, **kwargs)

    def is_connected(self):
        return bool(self.rpc)

    @property
    def prefix(self):
        return self.rpc.chain_params["prefix"]

    def info(self):
        """ Returns the global properties
        """
        return self.rpc.get_dynamic_global_properties()

    # -------------------------------------------------------------------------
    # Shared instance interface
    # -------------------------------------------------------------------------
    def set_shared_instance(self):
        """ This method allows to set the current instance as default
        """
        set_shared_blockchain_instance(self)

    @classmethod
    def get_shared_instance(cls, self):
        """ This interface allows to obtain the default instance
        """
        return shared_blockchain_instance()
