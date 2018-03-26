import sys, time, os, ast, csv
from similarity import Similarity
from wordpress import WordPressCMS
from screenshot import Screenshot

def list_to_string(obj):
    return str(obj).replace('[','').replace(']','').replace("'",'').strip()

wp = WordPressCMS(wp_path='../../../environment/wordpress/wordpress/')
screenshot = Screenshot(_dir='screenshots2')

with open('CONFLICTS_WP_SS') as f:
    CONFLICTS = ast.literal_eval(f.read())
    CONFLICTS = [
        ['a3-lazy-load', 'counterize']
        # ['comments-from-facebook', 'vk-all-in-one-expansion-unit'],
        # ['comments-from-facebook', 'disable-google-fonts'],
        # ['wp-author-date-and-meta-remover', 'comments-from-facebook'],
        # ['wp-author-date-and-meta-remover', 'vk-all-in-one-expansion-unit'],
    ]
    for conflict in CONFLICTS:
        wp.deactivate(conflict)

# capture screenshot from test page without plugins activated
default_page = '{}/default_page.png'.format(screenshot._dir)
print('capturing default page')
screenshot.capture(default_page)
print('capturing default end')

with open('visual_conflicts.csv', 'a+') as visual:
    visual_csv = csv.DictWriter(visual, fieldnames=['conflict', 'visual_effects'])
    visual_csv.writeheader()
    for conflict in CONFLICTS:
        print('running {}'.format(conflict))

        p1, p2 = conflict[0], conflict[1]
        _conflict = list_to_string(conflict)
        
        # creating a folder for each conflict
        conflict_dir = ''.join([screenshot._dir, '/', _conflict])
        screenshot.create_dir(conflict_dir)
                    
        # taking screenshot from first plugin
        try:
            wp.activate([p1])
            p1_path = '{}/{}.png'.format(conflict_dir, p1)
            print('capturing {} page'.format(p1))
            screenshot.capture(p1_path)
            print('capturing {} page end'.format(p1))
            
            # check similarity between
            wp.deactivate(conflict)

            # taking screenshot from second plugin
            wp.activate([p2])
            p2_path = '{}/{}.png'.format(conflict_dir, p2)
            print('capturing {} page'.format(p2))
            screenshot.capture(p2_path)
            print('capturing {} page end'.format(p2))

            # taking screenshot from both plugins (p2 already activated)
            wp.activate([p1])
            both_path = '{}/both.png'.format(conflict_dir)
            print('capturing conflict page')
            screenshot.capture(both_path)
            print('capturing conflict page end')
        except:
            # deactivating both plugins
            wp.deactivate(conflict)

        # deactivating both plugins
        wp.deactivate(conflict)
        
        # check similarity between images
        image_checker = Similarity(default_page, p1_path, p2_path, both_path, conflict_dir)
        is_changed = image_checker.is_changed_page()
                     
        visual_csv.writerow({'conflict': conflict, 'visual_effects': is_changed})
