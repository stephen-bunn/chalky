Adding an interface for producing styles and colors using chained properties.
Usage looks like this:

.. code-block:: python
    from chalk import chain

    print(chain.bold.blue | "I'm blue bold text!")
