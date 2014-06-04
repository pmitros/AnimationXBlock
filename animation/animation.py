"""TO-DO: Write a description of what this XBlock is."""

import json

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, List
from xblock.fragment import Fragment


class AnimationXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    animation = List(
        default=[], 
        scope=Scope.settings,
        help="Animation",
    )

    height = Integer(
        scope=Scope.settings,
        help="Height"
        )

    textheight = Integer(
        scope=Scope.settings,
        help="Text Height"
        )

    width = Integer(
        scope=Scope.settings,
        help="Width"
        )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AnimationXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/animation.html")
        frag = Fragment(html.format(height = self.height, textheight = self.textheight, width=self.width, animation = json.dumps(self.animation)))
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js")
        frag.add_css_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js")
        frag.add_css(self.resource_string("static/css/animation.css"))
        frag.add_javascript(self.resource_string("static/js/src/animation.js"))
        frag.initialize_js('AnimationXBlock')
        return frag

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        """
        Parse the XML for an HTML block.

        The entire subtree under `node` is re-serialized, and set as the
        content of the XBlock.

        """
        block = runtime.construct_xblock_from_class(cls, keys)
        animation = []

        element = {"desc":""} # Dummy; ignored
        for line in node.text.split('\n'):
            line = line.strip()
            if line.startswith("http"):
                element = {"src": line, "desc":""}
                animation.append(element)
            else:
                element["desc"] = element["desc"]  + " " + line


        block.animation = animation
        block.height = node.attrib["height"]
        block.textheight = node.attrib["textheight"]
        block.width = node.attrib["width"]

        return block


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AnimationXBlock",
             """<vertical_demo>
                <animation width="460" height="384" textheight="200">
http://upload.wikimedia.org/wikipedia/commons/e/e8/Pin_tumbler_no_key.svg
Without a key in the lock, the driver pins (blue) are pushed downwards, preventing the plug (yellow) from rotating.
http://upload.wikimedia.org/wikipedia/commons/5/54/Pin_tumbler_bad_key.svg
When an incorrect key is inserted into the lock, the key pins (red) and driver pins (blue) do not align with the shear line; therefore, it does not allow the plug (yellow) to rotate.
http://upload.wikimedia.org/wikipedia/commons/6/6e/Pin_tumbler_with_key.svg
When the correct key is inserted, the gaps between the key pins (red) and driver pins (blue) align with the edge of the plug (yellow).
http://upload.wikimedia.org/wikipedia/commons/e/e1/Pin_tumbler_unlocked.svg
With the gaps between the pins aligned with the shear line, the plug (yellow) can rotate freely.
                </animation>
                </vertical_demo>
             """),
        ]
