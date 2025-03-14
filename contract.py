# 💰 TIP JAR SMART CONTRACT 💰 : This smart contract allows users to send ALGO as tips, stores the total amount received, and tracks the last tipper's name.  The contract enforces a minimum tip amount, which can be updated by the owner, and provides functions to check tip stats. It also includes a debugging function to retrieve the last received tip amount for verification.  

# Import necessary modules from Algopy (Smart contract framework for Algorand)
# These modules help in defining contract logic, handling transactions, and storing state.
from algopy import ARC4Contract, UInt64, String, op
from algopy.arc4 import abimethod

# ---------------------------------------------------
# 💰 TIP JAR SMART CONTRACT 💰
# This smart contract allows users to send tips (in ALGO),
# keeps track of the total amount received, and records
# details such as the last tipper.
# ---------------------------------------------------

class TipJar(ARC4Contract):  # 🏦 This is our main smart contract class!
    # ---------------------------------------------------
    # 🛢️ STATE VARIABLES (Persistent Storage on Blockchain)
    # These variables will store important data about tips.
    # ---------------------------------------------------
    last_tipper: String      # 📌 Stores the name of the last person who tipped.
    total_tips: UInt64       # 📌 Tracks the total amount of ALGO received in tips.
    tip_count: UInt64        # 📌 Counts how many tips have been received.
    min_tip_amount: UInt64   # 📌 Defines the minimum tip required to send.
    debug_last_amount: UInt64  # 🐞 Debugging variable to store the last received tip amount.

    def __init__(self) -> None:  # 🏗️ Constructor: Initializes the contract with default values.
        """
        Initializes the contract with default values.
        This function is automatically executed when the contract is deployed.
        """
        self.last_tipper = String("")  # ❌ No tipper yet!
        self.total_tips = UInt64(0)    # 💵 No ALGO received yet!
        self.tip_count = UInt64(0)     # 🔢 No tips given yet!
        self.min_tip_amount = UInt64(1000)  # 🚦 Minimum tip is 0.001 ALGO (1,000 microAlgos).
        self.debug_last_amount = UInt64(0)  # 🐞 Debugging variable to track tip amounts.

    # ---------------------------------------------------
    # 💸 FUNCTION: Send a Tip
    # Allows users to send a tip by specifying their name and the tip amount.
    # ---------------------------------------------------
    @abimethod()
    def send_tip(self, name: String, amount: UInt64) -> None:
        """
        A user sends a tip by providing their name and tip amount.

        Parameters:
        - name (String): The name of the person sending the tip.
        - amount (UInt64): The ALGO amount being tipped.

        Raises:
        - AssertionError: If the tip amount is below the minimum required.
        """

        # 🐞 Store the received amount in a debug variable for logging purposes.
        self.debug_last_amount = amount  

        # 🛑 Ensure the tip meets the minimum requirement, or reject the transaction!
        assert amount >= self.min_tip_amount, "❌ Tip amount is too low!"

        # ✍️ Save the last tipper's name.
        self.last_tipper = name  

        # ➕ Add the tip amount to the total received.
        self.total_tips += amount  

        # 🔢 Increase the tip count.
        self.tip_count += 1  

    # ---------------------------------------------------
    # ⚙️ FUNCTION: Set Minimum Tip Amount
    # Allows the contract owner to update the minimum required tip.
    # ---------------------------------------------------
    @abimethod()
    def set_min_tip(self, amount: UInt64) -> None:
        """
        Sets a new minimum tip amount.

        Parameters:
        - amount (UInt64): The new minimum tip amount.

        Raises:
        - AssertionError: If the minimum tip amount is set to zero or negative.
        """
        assert amount > 0, "❌ Minimum tip must be greater than zero!"  # 🚦 Ensure it's a positive value.
        self.min_tip_amount = amount  # 🔄 Update the minimum tip amount.

    # ---------------------------------------------------
    # 🔍 FUNCTION: Retrieve Tip Information
    # Returns details about the last tipper, total tips, tip count, and min tip amount.
    # ---------------------------------------------------
    @abimethod()
    def get_tip_info(self) -> tuple[String, UInt64, UInt64, UInt64]:
        """
        Retrieves important contract information.

        Returns:
        - last_tipper (String): The name of the last person who tipped.
        - total_tips (UInt64): The total amount of ALGO received in tips.
        - tip_count (UInt64): The total number of tips received.
        - min_tip_amount (UInt64): The current minimum tip amount.
        """
        return self.last_tipper, self.total_tips, self.tip_count, self.min_tip_amount

    # ---------------------------------------------------
    # 🐞 FUNCTION: Retrieve Debugging Info
    # Allows you to check the last received tip amount (for debugging purposes).
    # ---------------------------------------------------
    @abimethod()
    def get_debug_info(self) -> UInt64:
        """
        Retrieves the last received tip amount for debugging.

        Returns:
        - debug_last_amount (UInt64): The last received tip amount.
        """
        return self.debug_last_amount  # 🕵️ Show the last received tip amount!
