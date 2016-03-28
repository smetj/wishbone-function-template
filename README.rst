::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ==========================
    wishbone.function.template
    ==========================

    Version: 1.0.0

    A Wishbone module which generates a text from a dictionary and a template.
    --------------------------------------------------------------------------


        Converts a dictionary to a text using the defined Jinja2 template.

        Optionally header template values can be converted too.


        Parameters:

            - location(str)("./")
               |  The directory containing templates.

            - template(str)()*
               |  The template filename stored in directory <location>.

            - source(str)("@data")*
               |  The dictionary to use.

            - destination(str)("@data")*
               |  The location to which the rendered result has to be stored.

            - header_templates(dict)({})*
               |  A dict of templates to render. Can be lookup values.
               |  Results are stored in this module's instance header
               |  using the provided key.



        Queues:

            - inbox
               |  Incoming events

            - outbox
               |  Outgoing events
