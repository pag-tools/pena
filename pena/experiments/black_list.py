#!/usr/bin/env python3

'''
Plugin list that show fatal errors when activated
'''

BLACK_LIST = [
    "woocommerce-improved-external-products",  # Total crash
    "we-will-call-you",  # Attempts to fetch external resource but fails to open stream
    "social-media-aggregator",  # Error when activated with wp-scroll-up
    "revcanonical",  # Uncaught Error: Call to undefined function spliti()
    "hooknews",  # Uncaught Error: Call to undefined function mysql_query()
    "cystats",  # Uncaught Error: Call to undefined function mysql_query()
    "easy-calendar",  # Uncaught Error: Call to undefined function spliti()
    "facebook",  # PHP Fatal error: 'break' not in the 'loop' or 'switch' context
    "less",  # PHP Fatal error:  Uncaught Error: Call to undefined function eregi_replace()
    "paypal-for-woocommerce",
    "quiz-master-next",
    "wp-force-ssl",
    "wp-force-https",
    "mailchimp-for-woocommerce",
    "eps-301-redirects",
    "ip-loc8",
    "our-team-enhanced",
    "easy-pie-coming-soon", # PHP Fatal error: Uncaught Error: Call to a member function set_background_type()
    "bad-behavior",
    "paid-memberships-pro",
    "accesspress-social-share",
    "head-cleaner",
    "wp-cerber",
    "bad-behavior"
]
