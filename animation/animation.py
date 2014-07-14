"""TO-DO: Write a description of what this XBlock is."""

import json

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, DateTime, Float
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

    position = Integer(
        scope=Scope.user_state,
        help="Current position",
        default=0
    )

    max_position = Integer(
        scope=Scope.user_state,
        help="Maximum position (for progress)",
        default=0
    )

    @XBlock.json_handler
    def update_position(self, data, suffix):
        if 'position' in data:
            self.position = data['position']
        if 'max_position' in data:
            self.max_position = data['max_position']
            grade = self.max_position/float(len(self.animation))
            self.runtime.publish(self, 'grade', {'value':grade, 'max_value': 1})
        return {"status":"success"}

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
        frag = Fragment(html.format(height = self.height, 
                                    textheight = self.textheight, 
                                    width=self.width, 
                                    inner_width=self.width-20, 
                                    animation = json.dumps(self.animation),
                                    position = self.position, 
                                    max_position = self.max_position))
#        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js")
        frag.add_css_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css")
        frag.add_css(self.resource_string("static/css/jquery.ui.labeledslider.css"))
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js")
        frag.add_javascript(self.resource_string("static/js/src/jquery.ui.labeledslider.js"))
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
                <animation width="460" height="384" textheight="100">
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
    ## Everything below is stolen from https://github.com/edx/edx-ora2/blob/master/apps/openassessment/xblock/lms_mixin.py
    ## It's needed to keep the LMS+Studio happy. 
    ## It should be included as a mixin. 
    ## 
    ## The only LMS functionality we need and use is grading. Cale
    ## believes most of this is unnecessary, but I did not want to do
    ## a binary search for what is and is not necessary, since this is
    ## effectively a TODO. 

    display_name = String(
        default="Completion", scope=Scope.settings,
        help="Display name"
    )

    start = DateTime(
        default=None, scope=Scope.settings,
        help="ISO-8601 formatted string representing the start date of this assignment. We ignore this."
    )

    due = DateTime(
        default=None, scope=Scope.settings,
        help="ISO-8601 formatted string representing the due date of this assignment. We ignore this."
    )

    weight = Float(
        display_name="Problem Weight",
        help=("Defines the number of points each problem is worth. "
              "If the value is not set, the problem is worth the sum of the "
              "option point values."),
        values={"min": 0, "step": .1},
        scope=Scope.settings
    )

    def has_dynamic_children(self):
        """Do we dynamically determine our children? No, we don't have any.
        """
        return False

    def max_score(self):
        """The maximum raw score of our problem.
        """
        return 1

