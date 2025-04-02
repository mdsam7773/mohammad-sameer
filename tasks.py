'''By default, Django signals are executed synchronously. This means that when a signal is sent, all connected receiver functions are executed one after another in the same thread and process before the code continues.

Proof via Code Snippet:
Here's a simple example that demonstrates synchronous execution:'''


from django.dispatch import Signal, receiver

# Create a signal
my_signal = Signal()

@receiver(my_signal)
def slow_receiver(sender, **kwargs):
    print("Slow receiver started")
    import time
    time.sleep(3)  # Simulate a slow operation
    print("Slow receiver finished")

@receiver(my_signal)
def fast_receiver(sender, **kwargs):
    print("Fast receiver started and finished")

print("Sending signal...")
my_signal.send(sender=None)
print("Signal send completed")


#Expected Output :-
'''
Sending signal...
Slow receiver started
Slow receiver finished
Fast receiver started and finished
Signal send completed
'''


#Task-2
'''
Yes, Django signals run in the same thread as the caller by default
 This means signal receivers execute synchronously in the same thread
where signal.send() is called, blocking further execution until all receivers 
finish.
'''

'''
Proof via Code Snippet
The following example demonstrates that signal handlers execute in the same thread as the caller by:

Printing the thread ID of the caller and the receivers.

Using a blocking operation (time.sleep()) to show sequential execution.

'''

from django.dispatch import Signal, receiver
import threading
import time

# Create a signal
my_signal = Signal()

@receiver(my_signal)
def receiver_1(sender, **kwargs):
    print(f"Receiver 1 - Thread ID: {threading.get_ident()}")
    time.sleep(2)  # Simulate work
    print("Receiver 1 finished")

@receiver(my_signal)
def receiver_2(sender, **kwargs):
    print(f"Receiver 2 - Thread ID: {threading.get_ident()}")
    print("Receiver 2 finished")

def main():
    print(f"Caller - Thread ID: {threading.get_ident()}")
    print("Sending signal...")
    my_signal.send(sender=None)
    print("Signal send completed")

if __name__ == "__main__":
    main()

#expected OUtput:
'''
Caller - Thread ID: 1234567890  # Same thread throughout
Sending signal...
Receiver 1 - Thread ID: 1234567890
Receiver 1 finished
Receiver 2 - Thread ID: 1234567890
Receiver 2 finished
Signal send completed    '''




#task_3
'''
By default, Django signals run in the same database transaction as the caller if the caller is inside an atomic transaction block. If no transaction is active, signals execute in autocommit mode (no transaction).

Imagine you’re transferring money between two bank accounts:

Step 1: Deduct money from Account A.

Step 2: A post_save signal (auto-triggered) adds money to Account B.

Step 3: Something fails, and the transaction rolls back.

What happens?

Both the deduction (Step 1) and the signal’s addition (Step 2) are canceled.

No money moves because the signal ran in the same transaction.


'''
from django.db import models, transaction

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.IntegerField(default=100)

# Signal: When BankAccount is saved, log the transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=BankAccount)
def log_transaction(sender, instance, **kwargs):
    print(f"💰 Log: {instance.name} now has ${instance.balance}")

# Transaction: Transfer $50 from Alice to Bob
try:
    with transaction.atomic():  # Start transaction
        alice = BankAccount.objects.get(name="Alice")
        bob = BankAccount.objects.get(name="Bob")

        alice.balance -= 50
        alice.save()  # Triggers post_save signal (logs Alice's balance)

        bob.balance += 50
        bob.save()  # Triggers post_save signal (logs Bob's balance)

        raise ValueError("Oops! Error!")  # Force rollback

except ValueError:
    print(" Transaction failed. Rolling back!")

# Check balances (should be unchanged)
alice = BankAccount.objects.get(name="Alice")
bob = BankAccount.objects.get(name="Bob")
print(f"Alice: ${alice.balance}, Bob: ${bob.balance}")
'''
What Happens?
The signal (log_transaction) runs immediately when .save() is called.

But since the transaction fails and rolls back:

The balance changes are undone.

The signal’s logs still print, but the database stays unchanged.

Key Takeaways
Signals run in the same transaction as the caller.

If the transaction fails, signal changes are rolled back too.

Signals can’t escape the transaction unless you use transaction.on_commit().




        Key Conclusions:-
Same Transaction: If the caller is in a transaction (atomic block),
 signal handlers do run in that transaction. Their DB changes commit/roll back with the caller’s.

 No Transaction: If the caller has no transaction (e.g., autocommit mode),
 signals execute immediately without transaction protection.

 Short Answer:
 Yes, by default, Django signals run in the same transaction as the code that triggers them.
   If the main code fails and rolls back, the signal’s changes also roll back.

        '''

#Topic: Custom Classes in Python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
    
    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

# Create a rectangle
rect = Rectangle(10, 20)

# Iterate over it
for dimension in rect:
    print(dimension)

 #output -    
'''
{'length': 10}
{'width': 20}'''