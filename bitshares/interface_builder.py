class BuilderInterface:

    def __init__(
        self,
        *args,
        chainspec=None,
        **kwargs
    ):

        assert chainspec

        # Legacy Proposal attributes
        self.proposer = kwargs.get("proposer", None)
        self.proposal_expiration = int(
            kwargs.get("proposal_expiration", 60 * 60 * 24))
        self.proposal_review = int(kwargs.get("proposal_review", 0))

        self._transactionbuildercls = chainspec.TransactionBuilder
        self._proposalbuildercls = chainspec.ProposalBuilder

        self.clear()

    # -------------------------------------------------------------------------
    # Transaction Buffers
    # -------------------------------------------------------------------------
    @property
    def txbuffer(self):
        """ Returns the currently active tx buffer
        """
        return self.tx()

    @property
    def propbuffer(self):
        """ Return the default proposal buffer
        """
        return self.proposal()

    def tx(self):
        """ Returns the default transaction buffer
        """
        return self._txbuffers[0]

    def proposal(
        self,
        proposer=None,
        proposal_expiration=None,
        proposal_review=None
    ):
        """ Return the default proposal buffer

            ... note:: If any parameter is set, the default proposal
               parameters will be changed!
        """
        if not self._propbuffer:
            return self.new_proposal(
                self.tx(),
                proposer,
                proposal_expiration,
                proposal_review
            )
        if proposer:
            self._propbuffer[0].set_proposer(proposer)
        if proposal_expiration:
            self._propbuffer[0].set_expiration(proposal_expiration)
        if proposal_review:
            self._propbuffer[0].set_review(proposal_review)
        return self._propbuffer[0]

    def new_proposal(
        self,
        parent=None,
        proposer=None,
        proposal_expiration=None,
        proposal_review=None,
        **kwargs
    ):
        if not parent:
            parent = self.tx()
        if not proposal_expiration:
            proposal_expiration = self.proposal_expiration

        if not proposal_review:
            proposal_review = self.proposal_review

        if not proposer:
            if "default_account" in self.config:
                proposer = self.config["default_account"]

        # Else, we create a new object
        proposal = self._proposalbuildercls(
            proposer,
            proposal_expiration,
            proposal_review,
            blockchain_instance=self,
            parent=parent,
            **kwargs
        )
        if parent:
            parent.appendOps(proposal)
        self._propbuffer.append(proposal)
        return proposal

    def new_tx(self, *args, **kwargs):
        """ Let's obtain a new txbuffer

            :returns int txid: id of the new txbuffer
        """
        builder = self._transactionbuildercls(
            *args,
            blockchain_instance=self,
            **kwargs
        )
        self._txbuffers.append(builder)
        return builder

    def clear(self):
        self._txbuffers = []
        self._propbuffer = []
        # Base/Default proposal/tx buffers
        self.new_tx()
        # self.new_proposal()
