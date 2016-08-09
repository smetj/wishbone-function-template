#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# template.py
#
#  Copyright 2013 Jelle Smet <jelle.smet@tomtom.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from jinja2 import Environment, FileSystemLoader
from jinja2 import Template as JinjaTemplate
from wishbone import Actor


class Template(Actor):

    '''**Generates a text from a dictionary and a template.**

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

    '''

    def __init__(self, actor_config, location="./", template=None, source="@data", destination="@data", header_templates={}):
        Actor.__init__(self, actor_config)

        self.pool.createQueue("inbox")
        self.pool.createQueue("outbox")
        self.registerConsumer(self.consume, "inbox")

    def preHook(self):

        if self.kwargs.template is not None:
            self.templates = Environment(loader=FileSystemLoader(self.kwargs.location))

    def consume(self, event):

        event = self.construct(event)
        self.submit(event, self.pool.queue.outbox)

    def construct(self, event):

        for name, template in self.kwargs.header_templates.items():
            try:
                template_r = JinjaTemplate(template)
                result = template_r.render(**event.get(self.kwargs.source))
                event.set(result, "@tmp.%s.%s" % (self.name, name))
            except Exception as err:
                self.logging.warning(
                    "Failed to convert header key '%s'.  Reason: %s" % (name, err))
                raise

        if self.kwargs.template is not None:
            try:
                template = self.templates.get_template(self.kwargs.template)
            except Exception as err:
                self.logging.error('No template found with filename "%s%s".' % (self.kwargs.location, self.kwargs.template))
                raise
            else:
                try:
                    result = template.render(**event.get(self.kwargs.source))
                    event.set(result, self.kwargs.destination)
                except Exception as err:
                    self.logging.error('There was an error processing the template. Reason: %s' % (err))
                    raise
        return event
