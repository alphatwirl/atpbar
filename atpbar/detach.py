# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
to_detach_pickup = False

##__________________________________________________________________||
def detach_pickup():
    """detach the pickup from any instances of `atpbar`

    If a pickup is started by an `atpbar` in the main thread of the
    main process, the pickup will be owned by the `atpbar`. The
    `atpbar` will end the pickup when the loop ends. This function
    detaches the pickup from the `atpbar` and prevents the atpbar from
    ending the pickup.

    This function is typically called by the pickup when the pickup
    receives a report from a sub-thread or a sub-process.

    """

    global to_detach_pickup
    to_detach_pickup = True
     # Locking here would causes a deadlock. `flush()` locks while
     # ending the pickup. Before receiving the end order, the pickup
     # might still receives a report with a new task ID from a
     # sub-thread or sub-process, it will call this function and will
     # cause a deadlock.


##__________________________________________________________________||
