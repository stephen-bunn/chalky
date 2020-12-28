Consuming the current chain's styles and colors if :method:`~.chain.Chain.chalk` is consumed.
This helps with constructing reusable styles with the chaining syntax:

.. code-block:: python
    :linenos:

    from chalky import chain

    # previously not possible
    error = chain.bold.white.bg.red
    success = chain.bold.bright_green

    # now possible
    error = chain.bold.white.bg.red.chalk
    success = chain.bold.bright_green.chalk
