"""Integration for CLIPS-style propositional logic."""



##### Classes #####



class CLIPS:
    """General class for all self-contained CLIPS instances."""

    def __init__(self):
        self.facts = []
        self.rules = []


    def DEFRULE(self, name: str, ):
        """Create a new logical relation."""


    def ASSERT(self):
        """Declare a new fact."""


    def RETRACT(self):
        """Retract an asserted fact."""


    def INFERENCE(self):
        """Run resolution on the entire database to a depth of `n`. If not provided runs until no more relations found."""


    def IMPLIES(self):
        """Logical implication."""


    def NOT(self):
        """Logical negation."""


    def DECLARE(self):
        """Declare a Boolean variable."""


    def RESET(self):
        """Reset the current CLIPS instance."""
        self.facts = []
        self.rules = []


    def WATCH(self):
        """Print new facts to standard output."""

    
    def UNWATCH(self):
        """Undo the `WATCH` function."""


def announce():
    """Create a new CLIPS instance."""


def renounce():
    """Destroy a created CLIPS instance."""
