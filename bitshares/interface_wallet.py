import logging

log = logging.getLogger(__name__)


class WalletInterface:
    def __init__(self, *args, chainspec=None, **kwargs):
        assert chainspec

        self.wallet = kwargs.get(
            "wallet",
            chainspec.Wallet(chainspec=chainspec, blockchain_instance=self, **kwargs),
        )

    # -------------------------------------------------------------------------
    # Wallet stuff
    # -------------------------------------------------------------------------
    def newWallet(self, pwd):
        """ Create a new wallet. This method is basically only calls
            :func:`bitshares.wallet.create`.

            :param str pwd: Password to use for the new wallet
            :raises bitshares.exceptions.WalletExists: if there is already a
                wallet created
        """
        return self.wallet.create(pwd)

    def unlock(self, *args, **kwargs):
        """ Unlock the internal wallet
        """
        return self.wallet.unlock(*args, **kwargs)
