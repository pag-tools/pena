from tname.core.visual_oracle.similarity import Similarity
import re, time

class VisualOracle:
    def __init__(self, conflicts, wordpress_cms, screenshot):
        self.conflicts = conflicts
        self.wp = wordpress_cms
        self.screenshot = screenshot
        self.visual_conflicts = []

    def formatting_line(self, obj):
        group = re.split("\[(.+)\]", str(obj))
        line = "".join(group).replace("'", "").replace('"',"")
        return line

    def run(self):
        # capture screenshot from test page without plugins activated
        default_page = "{}/default_page.png".format(self.screenshot.imgs_dir)
        self.screenshot.capture(default_page)
        for conflict in self.conflicts:
            images = []
            # creating a folder for each conflict
            _conflict = self.formatting_line(conflict)
            conflict_dir = "".join([self.screenshot.imgs_dir, "/", _conflict])
            self.screenshot.create_dir(conflict_dir)
            
            # take screenshot of all plugin individually activated
            for plugin in conflict:
                plugin_path = "{}/{}.png".format(conflict_dir, plugin)
                self.wp.activate([plugin])
                self.screenshot.capture(plugin_path)
                images.append(plugin_path)
                self.wp.deactivate([plugin])

            # take screenshot with conflict activated
            self.wp.activate(conflict)
            conflict_page = "{}/{}.png".format(conflict_dir, _conflict)
            self.screenshot.capture(conflict_page)
            self.wp.deactivate(conflict)

            image_checker = Similarity(
                default_page=default_page, 
                plugins_images=images, 
                conflict_page=conflict_page, 
                destination=conflict_dir
            )
            is_changed = image_checker.is_conflicting()

            if is_changed:
                print("visual conflict: {}".format(conflict))
                self.visual_conflicts.append(conflict)
        
        return self.visual_conflicts
