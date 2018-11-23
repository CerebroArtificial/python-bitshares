import logging

from .storage import get_default_config_store

# chain specific modules
from . import chainspec

from .interface_chain import TxInterface
from .interface_wallet import WalletInterface
from .interface_builder import BuilderInterface
from .interface_connection import InterfaceConnection

log = logging.getLogger(__name__)


class Chain(
    TxInterface,
    WalletInterface,
    InterfaceConnection,
    BuilderInterface
):
    """ Connect to the Blockchain network.

        ... note:: This module connects multiple interfaces together for sake
            of cleaner code separation. Please also lookup:

            * TxInterface,
            * WalletInterface,
            * InterfaceConnection,
            * BuilderInterface

        :param str node: Node to connect to *(optional)*
        :param str rpcuser: RPC user *(optional)*
        :param str rpcpassword: RPC password *(optional)*
        :param bool nobroadcast: Do **not** broadcast a transaction!
            *(optional)*
        :param bool debug: Enable Debugging *(optional)*
        :param array,dict,string keys: Predefine the wif keys to shortcut the
            wallet database *(optional)*
        :param bool offline: Boolean to prevent connecting to network (defaults
            to ``False``) *(optional)*
        :param str proposer: Propose a transaction using this proposer
            *(optional)*
        :param int proposal_expiration: Expiration time (in seconds) for the
            proposal *(optional)*
        :param int proposal_review: Review period (in seconds) for the proposal
            *(optional)*
        :param int expiration: Delay in seconds until transactions are supposed
            to expire *(optional)*
        :param str blocking: Wait for broadcasted transactions to be included
            in a block and return full transaction (can be "head" or
            "irrversible")
        :param bool bundle: Do not broadcast transactions right away, but allow
            to bundle operations *(optional)*

        Three wallet operation modes are possible:

        * **Wallet Database**: Here, the bitshareslibs load the keys from the
          locally stored wallet SQLite database (see ``storage.py``).
          To use this mode, simply call ``BitShares()`` without the
          ``keys`` parameter
        * **Providing Keys**: Here, you can provide the keys for
          your accounts manually. All you need to do is add the wif
          keys for the accounts you want to use as a simple array
          using the ``keys`` parameter to ``BitShares()``.
        * **Force keys**: This more is for advanced users and
          requires that you know what you are doing. Here, the
          ``keys`` parameter is a dictionary that overwrite the
          ``active``, ``owner``, or ``memo`` keys for
          any account. This mode is only used for *foreign*
          signatures!

        If no node is provided, it will connect to the node of
        http://uptick.rocks. It is **highly** recommended that you
        pick your own node instead. Default settings can be changed with:

        .. code-block:: python

            uptick set node <host>

        where ``<host>`` starts with ``ws://`` or ``wss://``.

        The purpose of this class it to simplify interaction with
        BitShares.

        The idea is to have a class that allows to do this:

        .. code-block:: python

            from bitshares import BitShares
            bitshares = BitShares()
            print(bitshares.info())

        All that is requires is for the user to have added a key with
        ``uptick``

        .. code-block:: bash

            uptick addkey

        and setting a default author:

        .. code-block:: bash

            uptick set default_account xeroc

        This class also deals with edits, votes and reading content.
    """

    # Below, we enable access to chain specific classes for those
    # classes we inherit

    def __init__(self,
                 node="",
                 rpcuser="",
                 rpcpassword="",
                 **kwargs):

        self.debug = bool(kwargs.get("debug", False))
        self.offline = bool(kwargs.get("offline", False))
        self.nobroadcast = bool(kwargs.get("nobroadcast", False))
        self.unsigned = bool(kwargs.get("unsigned", False))
        self.expiration = int(kwargs.get("expiration", 30))
        self.bundle = bool(kwargs.get("bundle", False))
        self.blocking = bool(kwargs.get("blocking", False))
        self.config = kwargs.get(
            "config_store",
            get_default_config_store()
        )

        # Initialize dependencies
        # We here provide "chainspec" as a module that contains
        # all classes that are chain-specific
        InterfaceConnection.__init__(
            self,
            node, rpcuser, rpcpassword,
            chainspec=chainspec,
            **kwargs)
        TxInterface.__init__(
            self,
            chainspec=chainspec,
            **kwargs
        )
        WalletInterface.__init__(self, 
            chainspec=chainspec,
            **kwargs)
        BuilderInterface.__init__(
            self,
            chainspec=chainspec,
            **kwargs)

    def set_blocking(self, block=True):
        """ This sets a flag that forces the broadcast to block until the
            transactions made it into a block
        """
        self.blocking = block


#: Legacy alias (deprecated)
BitShares = Chain
